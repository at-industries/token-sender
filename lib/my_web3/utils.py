from typing import Union, Optional
from web3.types import ChecksumAddress

import json


def read_json_from_file(path: str, encoding: Optional[str] = None) -> Union[list, dict]:
    return json.load(open(file=path, encoding=encoding))


def get_anonymous_string(address: Union[str, ChecksumAddress]) -> str:
    return str(address)[:5] + "..." + str(address)[-5:]
