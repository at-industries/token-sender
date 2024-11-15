# types
from typing import Any, Union, Tuple

# libraries
import random
import inspect

# lib
from lib.my_web3 import (
    TOKENS_DICT,
    NETWORKS_DICT,
)
from lib.my_excel import Sheet
from lib.my_web3 import MyWeb3, Token, Network

# core
from core.models.value import Value
from core.models.command import Command
from core.models.session import Session
from core.db import table_sessions as db


class Module:
    name: str
    sheet: Sheet

    def fill_data(self, data: dict):
        for attr in list(self.__annotations__):
            if attr in data:
                setattr(self, attr, data[attr])
        return self

    async def invoke(self, method_name: str, *args, **kwargs):
        return await getattr(self, method_name, None)(*args, **kwargs)

    async def check(self, log_process: str, account: dict) -> bool:
        return True

    async def create_commands(self, log_process: str, account: Any) -> list[Command]:
        return []

    def get_headers(self) -> list[str]:
        return list(self.__annotations__)

    def get_field(self, field_name: str) -> Any:
        return getattr(self, field_name, None)

    def get_tokens(self) -> list[Token]:
        return [TOKENS_DICT[attr_name] for attr_name in self.__annotations__ if attr_name in TOKENS_DICT]

    def get_networks(self) -> list[Network]:
        return [NETWORKS_DICT[attr_name] for attr_name in self.__annotations__ if attr_name in NETWORKS_DICT]

    def get_display(self, account: Any, command: Command) -> str:
        return ''

    def get_display_launcher(self, account: Any, command: Command) -> Union[str, Value]:
        return ''

    def get_display_software(self, account: Any, command: Command, start: bool) -> Tuple[Union[str, Value], Union[str, Value]]:
        return '', ''

    async def get_my_web3(
            self,
            account: Any,
            network: Network,
            async_provider: bool = False,
            proxy: Union[str, None] = None,
            gas_eth_max: Union[int, None] = None,
    ) -> Tuple[int, Union[MyWeb3, Exception]]:
        log_process = f'{inspect.currentframe().f_code.co_name}'
        try:
            my_web3 = MyWeb3(
                private_key=account.Main.private_key,
                async_provider=async_provider,
                proxy=proxy,
                gas_eth_max=gas_eth_max,
                network=network,
                gas_increase_base=1.5,
                gas_increase_gas=1.5,
            )
            status, result = await my_web3.is_connected()
            if status == 0:
                if result:
                    return 0, my_web3
                else:
                    return -1, Exception(f'{log_process} | {result}')
            else:
                return -1, Exception(f'{log_process} | {result}')
        except Exception as e:
            return -1, Exception(f'{log_process} | {e}')

    def save_command(self, session: Session, command) -> None:
        session.commands[command.index] = command
        db.change_session(session=session)

    def generate_random_float(self, left, right, precision) -> float:
        return round(random.uniform(left, right), precision)
