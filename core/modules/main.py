# lib
from lib.my_excel import Sheet

# core
from core.modules.constants import (
    NAME_MAIN,
)
from core.modules.module import Module


class Main(Module):
    private_key: str
    address: str
    proxy: str
    gas_eth_max: int
    thread: int

    Sleep: int
    Send: int
    Withdraw: int

    def __init__(self, ):
        self.name = NAME_MAIN
        self.sheet = Sheet(
            name=self.name,
            view=True,
            protected=False,
            headers=self.get_headers(),
        )
