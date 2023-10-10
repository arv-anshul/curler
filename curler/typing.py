from typing import Any, NamedTuple

from curler.constants import Method


class ParsedCurl(NamedTuple):
    method: str
    url: str
    data: str | None = None
    data_binary: str | None = None
    headers: dict = {}
    cookies: dict = {}
    insecure: bool = False
    user: tuple[str] | Any = ()
    proxy: dict[str, str] | str = {}
    compressed: bool = False
    include: bool = False
    silent: bool = False


http_method = Method()
