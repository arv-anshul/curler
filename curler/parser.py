import re
import urllib.parse
from http import cookies

from curler import typing
from curler.cli import get_curl_cli_parsed_args
from curler.typing import ParsedCurl, http_method


def parse_url(url: str) -> dict[str, list[str] | str]:
    parsed_url = urllib.parse.urlparse(url)
    query_params = urllib.parse.parse_qs(
        parsed_url.query,
        keep_blank_values=True,
    )
    return {k: v[0] if len(v) == 1 else v for k, v in query_params.items()}


def parse_cookies_headers(header: str) -> tuple[dict[str, str], dict[str, str]]:
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
            cookie = cookies.SimpleCookie(
                bytes(header_value, "ascii").decode("unicode-escape")
            )
            for key in cookie:
                cookie_dict[key] = cookie[key].value
        else:
            quoted_headers[header_key] = header_value.strip()

    return cookie_dict, quoted_headers


def parse_proxy(*, proxy: str, user: str) -> dict[str, str] | str:
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


def parse_curl(command: str, *, force_parse: bool = False):
    # Clean curl command to be safe
    command = command.replace("\\", "")

    parsed = get_curl_cli_parsed_args(command)

    method = parsed.X
    if parsed.data_binary:
        method = http_method.POST

    if not force_parse:
        if parsed.X.upper() not in http_method._asdict().keys():
            raise NotImplementedError(
                f"Method {parsed.X.upper()} is not implemented. "
                "If you want to force_parse then pass the argument for that."
            )
    else:
        method = parsed.X.upper()

    user = parsed.user
    if user:
        user = tuple(user.split(":"))

    proxies = parse_proxy(proxy=parsed.proxy, user=parsed.user)
    cookie_dict, quoted_headers = parse_cookies_headers(parsed.header)

    return ParsedCurl(
        method=method,
        url=parsed.url.split("?", 1)[0],
        params=parse_url(parsed.url),
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


def parse_file(fp: typing.PathLike) -> ParsedCurl:
    with open(fp) as f:
        return parse_curl(f.read())
