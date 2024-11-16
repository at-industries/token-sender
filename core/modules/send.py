# types
from typing import Any, Union, Tuple
from web3.types import HexBytes

# libraries
import random
import inspect

# lib
from lib.my_web3 import (
    NETWORKS_DICT
)
from lib.my_excel import Sheet
from lib import my_logger as logger
from lib.my_web3 import MyWeb3, Network

# core
from core.modules.constants import (
    NAME_SEND,
)
from core.models.value import (
    OK,
    DEFAULT,
)
from core.models.value import Value
from core.modules.module import Module
from core.models.session import Session, Command

# utils
from utils import utils
from lib.my_web3.utils import get_anonymous_string


class Send(Module):
    address_out: str
    percent_min: float
    percent_max: float
    amount_min: float
    amount_max: float
    network: str
    address_token: str

    DAI: int
    USDC: int
    USDCe: int
    USDT: int
    WETH: int

    def __init__(self, ):
        self.name = NAME_SEND
        self.sheet = Sheet(
            name=self.name,
            view=True,
            protected=False,
            headers=self.get_headers(),
        )
        self.tokens = self.get_tokens()

    async def get_display(self, account: Any, command: Command) -> str:
        address_token = command.info[1]
        network = NETWORKS_DICT[command.info[0]]
        w3 = MyWeb3(network=network)
        status, result = await w3.ERC20_get_token_symbol_by_address_smart(address_token)
        if status == -1:
            symbol = get_anonymous_string(address_token)
        else:
            symbol = result
        return f'{self.name}({symbol}_from_{network.name}_to_{get_anonymous_string(self.address_out)})'

    async def get_display_launcher(self, account: Any, command: Command) -> Union[str, Value]:
        display = await self.get_display(account=account, command=command)
        if command.function == self.send_complete.__name__:
            return display
        else:
            return DEFAULT

    async def get_display_software(self, account: Any, command: Command, start: bool) -> Tuple[Union[str, Value], Union[str, Value]]:
        display = await self.get_display(account=account, command=command)
        if start:
            if command.function == self.send_complete.__name__:
                return display, DEFAULT
            elif command.function == self.send_verify.__name__:
                return display, display
            else:
                return DEFAULT, DEFAULT
        else:
            if command.function == self.send_complete.__name__:
                return display, DEFAULT
            elif command.function == self.send_verify.__name__:
                return DEFAULT, display
            else:
                return DEFAULT, DEFAULT

    async def create_commands(self, log_process: str, account: Any) -> list[Command]:
        commands = []
        tokens = []
        functions = [
            self.send_complete,
            self.send_verify,
        ]
        for token in self.tokens:
            if getattr(self, token.name, 0) == 1:
                tokens.insert(random.randint(0, len(tokens)), token)
        if self.address_token is not None:
            for func in functions:
                commands.append(Command(module=self.name, function=func.__name__, info=(self.network, self.address_token)))
        for token in tokens:
            for func in functions:
                commands.append(Command(module=self.name, function=func.__name__, info=(self.network, token.addresses[NETWORKS_DICT[self.network]])))
        return commands

    @utils.log_function(level=logger.DEB)
    async def send_complete(self, log_process: str, session: Session, command: Command, account: Any) -> bool:
        log_process = f'{log_process} | {inspect.currentframe().f_code.co_name}'
        try:
            network: Network = NETWORKS_DICT[command.info[0]]
            address_token: str = command.info[1]

            status, result = await self.get_my_web3(account=account, network=network)
            if status == -1:
                utils.log_error(f'{log_process} | {result}')
                return False
            my_web3: MyWeb3 = result

            status, result = await my_web3.ERC20_get_balance(address_token=address_token)
            if status == -1:
                utils.log_error(f'{log_process} | {result}')
                return False
            balance: int = result

            if balance == 0:
                command.value = HexBytes(0)
                command.status = OK
                self.save_command(session, command)
                return True

            if (self.percent_min == 100) and (self.percent_max == 100):
                amount = balance
            elif (self.percent_min is not None) and (self.percent_max is not None):
                amount = int(balance * (self.generate_random_float(self.percent_min, self.percent_max, 2) / 100))
            else:
                status, result = await my_web3.ERC20_get_decimals_smart(address_token=address_token)
                if status == -1:
                    utils.log_error(f'{log_process} | {result}')
                    return False
                decimals: int = result
                amount = int(self.generate_random_float(self.amount_min, self.amount_max, precision=decimals) * 10 ** decimals)

            status, result = await my_web3.ERC20_transfer_amount(amount=amount, address_token=address_token, address_recipient=self.address_out)
            if status == -1:
                utils.log_error(f'{log_process} | {result}')
                return False
            tx: HexBytes = result

            command.value = tx
            command.status = OK
            self.save_command(session, command)
            return True

        except Exception as e:
            utils.log_error(f'{log_process} | {e}')
            return False

    @utils.log_function(level=logger.DEB)
    async def send_verify(self, log_process: str, session: Session, command: Command, account: Any) -> bool:
        log_process = f'{log_process} | {inspect.currentframe().f_code.co_name}'
        try:
            status, result = await self.get_my_web3(account=account, network=NETWORKS_DICT[command.info[0]])
            if status == -1:
                utils.log_error(f'{log_process} | {result}')
                return False
            my_web3: MyWeb3 = result

            command_previous = session.commands[command.index - 1]
            tx: HexBytes = HexBytes(command_previous.value)

            if tx == HexBytes(0):
                command.status = OK
                self.save_command(session, command)
                utils.log_info(f'{log_process} | Balance: 0')
                return True

            status, result = await my_web3.verify_transaction(transaction_hash=tx)
            if status == -1:
                utils.log_error(f'{log_process} | {result}')
                return False
            check: bool = result

            if not check:
                utils.log_error(f'{log_process} | {check}')
                return False

            command.status = OK
            self.save_command(session, command)
            return True

        except Exception as e:
            utils.log_error(f'{log_process} | {e}')
            return False
