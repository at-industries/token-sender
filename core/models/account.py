# types
from typing import Any

# core
from core.modules import *


class Account:
    index: int
    Main: Main
    Sleep: Sleep
    Send: Send
    Withdraw: Withdraw

    def fill_data(self, data: dict):
        for attr in list(self.__annotations__):
            if attr in data:
                setattr(self, attr, data[attr])
        return self

    def get_field(self, field_name: str) -> Any:
        return getattr(self, field_name, None)
