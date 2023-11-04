import os
import typing as t
from pathlib import Path

from curler.constants import Method


class CurlForRequests(t.TypedDict):
    method: str
    url: str
    params: dict[str, list[str] | str]
    data: str | None
    data_binary: str | None
    headers: dict
    cookies: dict
    user: tuple[str] | t.Any
    proxy: dict[str, str] | str


class ParsedCurl(t.NamedTuple):
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
    def for_requests(self) -> CurlForRequests:
        return CurlForRequests(
            **{
                k: v
                for k, v in self._asdict().items()
                if k in CurlForRequests.__annotations__.keys() and v
            }
        )


http_method = Method()
PathLike: t.TypeAlias = str | os.PathLike | Path
