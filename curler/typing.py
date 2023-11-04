import os
import typing as t
from pathlib import Path

from curler.constants import Method


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


http_method = Method()
PathLike: t.TypeAlias = str | os.PathLike | Path
