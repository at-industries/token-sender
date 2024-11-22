# types
import asyncio
from typing import Union, Optional

# libraries
import inspect
import time
import sys

# lib
from lib.my_excel import MyExcel
from lib import my_logger as logger
from lib.my_web3.models.network import NETWORK_NAMES_LIST
from lib.my_web3.models.token import TOKENS_DICT, Token, TOKENS_LIST
from lib.my_web3.myweb3 import MyWeb3
from lib.my_web3.models.network import Network, NETWORKS_DICT
from lib.my_csv.mycsv import MyCSV

# core
from core.models import Data
from core.models.account import Account
from core.modules import Main, Send

# data
from data.constants import BATCH_SIZE

# utils
from utils import utils


class Checker:
    process = 'CHECKER'

    def __init__(self, log_process: str, soft_data: Data, excel: MyExcel):
        self.process = f'{log_process} | {self.process}'
        self.soft_data = soft_data
        self.excel = excel
        self.table = {}
        self.accounts = []
        self.addresses = []
        self.my_web3: MyWeb3
        self.batch_size = BATCH_SIZE
        self.network: Optional[Network] = None

    async def __aenter__(self, ):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        return

    async def start(self, ) -> None:
        if not await self.load_table(self.process):
            return
        if not await self.load_accounts(self.process):
            return
        if not await self.network_choice(self.process):
            return

    @utils.log_function(level=logger.DEB)
    async def load_table(self, log_process: str) -> Union[bool, dict]:
        status, result = self.excel.get_table_as_dict()
        if status == 0:
            table = dict(result)
            if not table:
                return False
            else:
                self.table = table
                return True
        else:
            utils.log_error(f'{log_process} | {inspect.currentframe().f_code.co_name} | {result}')
            return False

    @utils.log_function(level=logger.DEB)
    async def load_accounts(self, log_process: str) -> bool:
        if not await self._load_accounts_dicts(f'{log_process} | {inspect.currentframe().f_code.co_name}'):
            return False
        if not await self._load_accounts_objects(f'{log_process} | {inspect.currentframe().f_code.co_name}'):
            return False
        return True

    @utils.log_function(level=logger.DEB)
    async def _load_accounts_dicts(self, log_process: str) -> bool:
        accounts = []
        data = self.table
        for i in range(len(next(iter(data.values())))):
            account = {}
            for module_name, accounts_list in data.items():
                if module_name in [Main().name, Send().name]:
                    account[module_name] = accounts_list[i]
            accounts.append(account)
        if not accounts:
            return False
        else:
            self.accounts = accounts
            return True

    @utils.log_function(level=logger.DEB)
    async def _load_accounts_objects(self, log_process: str) -> bool:
        accounts = [Account() for _ in range(len(self.accounts))]
        for i in range(len(accounts)):
            data = {}
            for module_name, module_type in self.soft_data.modules_dict.items():
                if module_name in [Main().name, Send().name]:
                    if module_type().sheet.view:
                        module = module_type().fill_data(data=self.accounts[i][module_name])
                        data[module_name] = module
            accounts[i].fill_data(data=data)
            accounts[i].index = i
        if not accounts:
            return False
        else:
            self.accounts = accounts
            return True

    async def network_choice(self, log_process: str) -> bool:
        time.sleep(1)
        print(f"Choose a number of the network where you want to check addresses' balances:")
        print(utils.create_options_list_with_numbers(NETWORK_NAMES_LIST))
        print(f'close = stop the soft.')
        while True:
            answer = input()
            try:
                answer = int(answer)
                if 0 < answer <= len(NETWORK_NAMES_LIST):
                    network_name = NETWORK_NAMES_LIST[answer-1]
                    self.network = NETWORKS_DICT[network_name]
                    while True:
                        async with self as checker:
                            await checker.start_checker()
                        break
                    break
                else:
                    print(f'Input number is out of the available range, choose a number from the list above!')
            except ValueError:
                if answer.lower() == 'close':
                    break
                else:
                    print(f'Input must be an integer, from the list above!')
        return True

    async def start_checker(self, ) -> None:
        if not await self._fill_addresses(self.process):
            return
        if not await self._fill_accounts(self.process):
            return
        if not await self._create_csv(self.process):
            return

    async def _fill_addresses(self, log_process: str) -> bool:
        addresses = []
        for account in self.accounts:
            address_info = {'address': account.Main.address, 'user_token': account.Send.address_token}
            addresses.append(address_info)
        if not addresses:
            return False
        else:
            self.addresses = addresses
            return True

    async def _fill_accounts(self, log_process: str) -> bool:
        self.my_web3 = MyWeb3(network=self.network, async_provider=True)
        results = await self.get_accounts_info()
        accounts_list = self.pack_results(results)
        self.accounts = [self._get_headers()] + accounts_list
        return True

    async def get_accounts_info(self, ) -> list:
        address_user_token = self.accounts[0].Send.address_token
        if address_user_token is not None:
            tokens_qty = 6
            tasks_qty = len(self.addresses) * tokens_qty
        else:
            tokens_qty = 5
            tasks_qty = len(self.addresses) * tokens_qty
        results = []
        batch_tasks = []
        progress_bar(len(results), tasks_qty, tokens_qty)

        for address_info in self.addresses:
            address_wallet = address_info['address']
            for token in TOKENS_LIST:
                if len(batch_tasks) == self.batch_size:
                    results += await asyncio.gather(*batch_tasks)
                    batch_tasks = []
                    await asyncio.sleep(1)
                batch_tasks.append(asyncio.create_task(self._get_token_balance(token=token, address=address_wallet)))
            if address_user_token is not None:
                if len(batch_tasks) == self.batch_size:
                    results += await asyncio.gather(*batch_tasks)
                    batch_tasks = []
                    await asyncio.sleep(1)
                batch_tasks.append(asyncio.create_task(self._get_user_token_balance(address_token=address_user_token, address_wallet=address_wallet)))
            progress_bar(len(results), tasks_qty, tokens_qty)
        if batch_tasks is not None:
            results += await asyncio.gather(*batch_tasks)
            progress_bar(len(results), tasks_qty, tokens_qty)
        print()  # new line after progress_bar
        return results

#    async def _check_batch(self, results: list, batch_tasks: list) -> Tuple[list, list]:  # ToDo: увеличивает кол-во операций
#        if len(batch_tasks) == self.batch_size:
#            results += await asyncio.gather(*batch_tasks)
#            batch_tasks = []
#            await asyncio.sleep(1)
#            return results, batch_tasks
#        return results, batch_tasks

    async def _get_token_balance(self, token: Token, address: str):
        status, result = await self.my_web3.ERC20_get_balance(
            address_wallet=address,
            address_token=token.addresses[self.network]
        )
        if status == 0:
            token_balance = result / 10 ** token.decimals
        else:
            token_balance = 'failed to get balance'
        return token_balance

    async def _get_user_token_balance(self, address_token: str, address_wallet: str):
        status, result = await self.my_web3.ERC20_get_balance(
            address_wallet=address_wallet,
            address_token=address_token
        )
        if status == 0:
            token_balance = result / 10 ** 9
        else:
            token_balance = 'failed to get balance'
        return token_balance

    def pack_results(self, results: list) -> list[list]:
        index = 1
        accounts_list = []
        user_address_token = self.accounts[0].Send.address_token
        if user_address_token is not None:
            for i in range(0, len(results), 6):
                accounts_list.append([index, self.addresses[index-1]['address']] + results[i:i+6])
                index += 1
        else:
            for i in range(0, len(results), 5):
                accounts_list.append([index, self.addresses[index-1]['address']] + results[i:i+5])
                index += 1
        return accounts_list

    @staticmethod
    def _get_headers() -> list[str]:
        headers = ['index', 'address', 'user token']
        for token_name in TOKENS_DICT.keys():
            headers.insert(len(headers) - 1, token_name)
        return headers

    async def _create_csv(self, log_process: str):
        my_csv = MyCSV()
        status, result = my_csv.create_file(data=self.accounts, addition_to_filepath=self.network.name.upper())
        if status == -1:
            utils.log_error(f'{log_process} | {result}')
            return False
        else:
            utils.log_info(f'{log_process} | {result}')
            return True


def progress_bar(iteration, total, tokens_qty, length=40):
    total //= tokens_qty
    iteration //= tokens_qty
    percent = (iteration / total)
    arrow = '█' * int(length * percent)
    spaces = ' ' * (length - len(arrow))
    sys.stdout.write(f'\r|{arrow}{spaces}| {percent:.0%} | КОШЕЛЬКОВ ОБРАБОТАНО: {iteration}/{total}')
    sys.stdout.flush()
