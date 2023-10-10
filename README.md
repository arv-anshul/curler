# curler

Import curl command in python and use it with requests, httpx, etc. libraries.

## Installation

```sh
pip install curler
```

```python
from curler import curl_command_parser

curl = (
    "curl "
    "'https://pypi.python.org/project/arv-easy-analysis' "
    "-H 'Accept-Encoding:gzip,deflate,sdch' "
    "-H 'Accept-Language:en-US,en;q=0.8'"
)
curl_command_parser(curl)
```

```python
# Output:

ParsedCurl(
    method='GET',
    url='https://pypi.python.org/project/arv-easy-analysis',
    data=None,
    data_binary=None,
    headers=OrderedDict([('Accept-Encoding', 'gzip,deflate,sdch'), ('Accept-Language', 'en-US,en;q=0.8')]),
    cookies=OrderedDict(),
    insecure=False,
    user=(),
    proxy={},
    compressed=False,
    include=False,
    silent=False
)
```

## Acknowledgment

- 🤗 This package is heavily inspired by [@spulec/uncurl](https://github.com/spulec/uncurl).
