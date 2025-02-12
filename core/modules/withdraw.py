# types
from typing import Any, Union, Tuple
from web3.types import HexBytes

# libraries
import random
import inspect

# lib
from lib.my_web3 import (
    NETWORKS_DICT,
    TOKENS_DICT,
)
from lib.my_excel import Sheet
from lib import my_logger as logger
from lib.my_web3 import MyWeb3, Network

# core
from core.modules.constants import NAME_WITHDRAW
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


class Withdraw(Module):
    address_out: str
    percent_min: float
    percent_max: float
    amount_min: float
    amount_max: float

    Arbitrum: int
    Avalanche: int
    Base: int
    BSC: int
    Celo: int
    Ethereum: int
    Fantom: int
    Linea: int
    Moonbeam: int
    Moonriver: int
    Optimism: int
    Polygon: int
    Polygon_zkEVM: int
    Scroll: int
    zkSync: int

    def __init__(self, ):
        self.name = NAME_WITHDRAW
        self.sheet = Sheet(
            name=self.name,
            view=True,
            protected=False,
            headers=self.get_headers(),
        )
        self.networks = self.get_networks()

    async def get_display(self, account: Any, command: Command) -> str:
        network = NETWORKS_DICT[command.info[0]]
        symbol = network.coin.name
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
        networks = []
        functions = [
            self.send_complete,
            self.send_verify,
        ]
        for network in self.networks:
            if getattr(self, network.name, 0) == 1:
                networks.insert(random.randint(0, len(networks)), network)
        for network in networks:
            for func in functions:
                commands.append(Command(module=self.name, function=func.__name__, info=(network.name, )))
        return commands

    @utils.log_function(level=logger.DEB)
    async def send_complete(self, log_process: str, session: Session, command: Command, account: Any) -> bool:
        log_process = f'{log_process} | {inspect.currentframe().f_code.co_name}'
        try:
            network: Network = NETWORKS_DICT[command.info[0]]

            status, result = await self.get_my_web3(account=account, network=network)
            if status == -1:
                utils.log_error(f'{log_process} | {result}')
                return False
            my_web3: MyWeb3 = result

            status, result = await my_web3.get_balance()
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
                decimals = network.coin.n_decimals
                amount = int(self.generate_random_float(self.amount_min, self.amount_max, precision=decimals) * 10 ** decimals)
            status, result = await my_web3.transfer_amount(amount=amount, address_recipient=self.address_out)
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
