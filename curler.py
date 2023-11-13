"""
`curler` is a lightweight package to parse curl commands to use them in python.

🧩 Usage
---
>>> import curler
>>> command = 'curl -X POST -d "data" http://example.com'
>>> parsed_curl = curler.parse_curl(command)
>>> parsed_curl.method
'POST'
>>> parsed_curl.url
'http://example.com'

😎 Credits
---
🧑‍💻 Author: https://github.com/arv-anshul/
🌐 Homepage: https://github.com/arv-anshul/curler/
"""

import argparse
import http.cookies
import os
import re
import shlex
import typing as t
import urllib.parse
from pathlib import Path

PathLike: t.TypeAlias = str | os.PathLike | Path


class ParsedCurl(t.NamedTuple):
    """Represents the parsed information from a curl command."""

    method: str
    url: str
    params: dict[str, list[str] | str] = {}
    data: str | None = None
    data_binary: str | None = None
    headers: dict = {}
    cookies: dict = {}
    insecure: bool = False
    user: tuple[str] | t.Any = ()
    proxy: dict[str, str] | str = {}
    compressed: bool = False
    include: bool = False
    silent: bool = False

    @property
    def for_requests(self) -> dict[str, t.Any]:
        """
        Returns a dictionary containing relevant information for making requests
        with the `requests` library.
        """
        keys__ = [
            "method",
            "url",
            "params",
            "data",
            "data_binary",
            "headers",
            "cookies",
            "user",
            "proxy",
        ]
        return {k: v for k, v in self._asdict().items() if k in keys__ and v}


def get_params_from_url(url: str) -> dict[str, list[str] | str]:
    """
    Extracts query parameters from a URL.

    Args:
      url: Input URL

    Returns:
      A dictionary containing query parameters.
    """
    parsed_url = urllib.parse.urlparse(url)
    query_params = urllib.parse.parse_qs(
        parsed_url.query,
        keep_blank_values=True,
    )
    return {k: v[0] if len(v) == 1 else v for k, v in query_params.items()}


def get_cookies_headers(header: str) -> tuple[dict[str, str], dict[str, str]]:
    """
    Extracts cookies and headers from a string.

    Args:
      header: Input header string

    Returns:
      A tuple containing dictionaries for cookies and headers.
    """
    cookie_dict = {}
    quoted_headers = {}

    for curl_header in header:
        if curl_header.startswith(":"):
            occurrence = [m.start() for m in re.finditer(":", curl_header)]
            header_key, header_value = (
                curl_header[: occurrence[1]],
                curl_header[occurrence[1] + 1 :],
            )
        else:
            header_key, header_value = curl_header.split(":", 1)

        if header_key.lower().strip("$") == "cookie":
            cookie = http.cookies.SimpleCookie(
                bytes(header_value, "ascii").decode("unicode-escape")
            )
            for key in cookie:
                cookie_dict[key] = cookie[key].value
        else:
            quoted_headers[header_key] = header_value.strip()

    return cookie_dict, quoted_headers


def get_proxy(*, proxy: str, user: str) -> dict[str, str] | str:
    """
    Generates proxy information based on the provided proxy and user details.

    Args:
      proxy: Proxy URL
      user: User details for authentication

    Returns:
      Proxy information as a dictionary or a string.
    """
    proxies = proxy
    if proxy and user:
        proxies = {
            "http": f"http://{user}@{proxy}/",
            "https": f"https://{user}@{proxy}/",
        }
    elif proxy:
        proxies = {
            "http": f"http://{proxy}/",
            "https": f"https://{proxy}/",
        }
    return proxies


def parse_curl(command: str):
    """
    Parses a curl command and returns the corresponding `ParsedCurl` object.

    Args:
      command: Input curl command

    Returns:
      A `ParsedCurl` object representing the parsed information.
    """
    # Clean curl command to be safe
    command = command.replace("\\", "")

    parsed = get_curl_cli_parsed_args(command)

    method = parsed.X
    if parsed.data_binary:
        method = "POST"
    else:
        method = parsed.X.upper()

    user = parsed.user
    if user:
        user = tuple(user.split(":"))

    proxies = get_proxy(proxy=parsed.proxy, user=parsed.user)
    cookie_dict, quoted_headers = get_cookies_headers(parsed.header)

    return ParsedCurl(
        method=method,
        url=parsed.url.split("?", 1)[0],
        params=get_params_from_url(parsed.url),
        data=parsed.data,
        data_binary=parsed.data_binary,
        headers=quoted_headers,
        cookies=cookie_dict,
        insecure=parsed.insecure,
        user=user,
        proxy=proxies,
        compressed=parsed.compressed,
        include=parsed.include,
        silent=parsed.silent,
    )


def parse_file(fp: PathLike) -> ParsedCurl:
    """
    Parses a curl command from a file and returns the corresponding `ParsedCurl` object.

    Args:
      fp: File path

    Returns:
      A `ParsedCurl` object representing the parsed information.
    """
    with open(fp) as f:
        return parse_curl(f.read())


# --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- #
# Command line parsing
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- #
def _basic_validation_on_command(command: str) -> None:
    """
    Performs basic validation on the input curl command.

    Args:
      command: Input curl command

    Raises:
      AssertionError: If the command does not start with "curl".
    """
    assert (
        command.split(" ", 1)[0] == "curl"
    ), 'Start with curl command. Like "curl https://example.com/"'


def get_curl_cli_parsed_args(command: str) -> argparse.Namespace:
    """
    Parses the input curl command and returns the parsed arguments.

    Args:
      command: Input curl command

    Returns:
      Parsed arguments as a namespace.
    """
    _basic_validation_on_command(command)
    tokens = shlex.split(command)
    parsed = curl_parser.parse_args(tokens)
    return parsed


curl_parser = argparse.ArgumentParser()

curl_parser.add_argument("command", help="Start the command with `curl`.")
curl_parser.add_argument("url")
curl_parser.add_argument("-d", "--data")
curl_parser.add_argument("-b", "--data-binary", "--data-raw", default=None)
curl_parser.add_argument("-X", default="GET")
curl_parser.add_argument("-H", "--header", action="append", default=[])
curl_parser.add_argument("--compressed", action="store_true")
curl_parser.add_argument("-k", "--insecure", action="store_true")
curl_parser.add_argument("-U", "--user", default=())
curl_parser.add_argument("-i", "--include", action="store_true")
curl_parser.add_argument("-s", "--silent", action="store_true")
curl_parser.add_argument("-x", "--proxy", default={})
