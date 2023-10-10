import argparse
import shlex

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


def _basic_validation_on_command(command: str) -> None:
    assert (
        command.split(" ", 1)[0] == "curl"
    ), 'Start with curl command. Like "curl https://example.com/"'


def get_curl_parsed_args(command: str) -> argparse.Namespace:
    _basic_validation_on_command(command)
    tokens = shlex.split(command)
    parsed = curl_parser.parse_args(tokens)
    return parsed
