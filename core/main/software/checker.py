# types
import asyncio
from typing import Union, Optional

# libraries
import inspect
import time

# lib
from lib.my_excel import MyExcel
from lib import my_logger as logger
from lib.my_web3.models.network import NETWORK_NAMES_LIST
from lib.my_web3.models.token import TOKENS_DICT
from lib.my_web3.myweb3 import MyWeb3
from lib.my_web3.models.network import Network, NETWORKS_DICT
from lib.my_csv.mycsv import MyCSV

# core
from core.models import Data
from core.models.account import Account
from core.modules import Main, Send

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

        tasks = []
        for address_info in self.addresses:
            task = asyncio.create_task(self._get_account_balances(log_process=log_process, address_info=address_info))
            tasks.append(task)
        balances = list(await asyncio.gather(*tasks))

        if balances:
            accounts = await self._get_filled_accounts(balances=balances, log_process=log_process)
            if accounts:
                self.accounts = accounts
                return True
            else:
                utils.log_error(f'{inspect.currentframe().f_code.co_name} | {log_process}')
                return False
        else:
            utils.log_error(f'{inspect.currentframe().f_code.co_name} | {log_process}')
            return False

    async def _get_account_balances(self, log_process: str, address_info: dict) -> dict:
        address = address_info['address']
        user_token = address_info['user_token']
        default_tokens_balances = await self._get_default_tokens_balances(log_process=log_process, address=address)
        user_token_balance = await self._get_user_token_balance(log_process=log_process, address=address, user_token=user_token)
        token_balances = {**default_tokens_balances, **user_token_balance}
        return token_balances

    async def _get_default_tokens_balances(self, log_process: str, address: str) -> dict:
        token_balances = {}
        try:
            for token in TOKENS_DICT.values():
                status, result = await self.my_web3.ERC20_get_balance(
                    address_wallet=address,
                    address_token=token.addresses[self.network]
                )
                if status == 0:
                    token_balance = result
                    token_balances[token.name] = token_balance / 10 ** token.decimals
                else:
                    token_balances[token.name] = 'failed to get balance'
            return token_balances
        except Exception as e:
            utils.log_error(f'{log_process} | {inspect.currentframe().f_code.co_name} | {e}')
            return {}

    async def _get_user_token_balance(self, log_process: str, address: str, user_token: str) -> dict:
        token_balances = {}
        try:
            if user_token is not None:
                status, result = await self.my_web3.ERC20_get_balance(
                    address_wallet=address,
                    address_token=user_token
                )
                if status == 0:
                    user_token_balance = result
                    status, result = await self.my_web3.ERC20_get_decimals_smart(user_token)
                    if status == 0:
                        decimals = result
                        token_balances['user_token'] = user_token_balance / 10 ** decimals
                    else:
                        token_balances['user_token'] = 'failed to get token decimals'
                else:
                    token_balances['user_token'] = 'failed to get balance'
            else:
                token_balances['user_token'] = ''
            return token_balances
        except Exception as e:
            utils.log_error(f'{log_process} | {e}')
            return {}

    async def _get_filled_accounts(self, balances: list, log_process: str) -> list:
        accounts = [self._get_headers()]
        try:
            for i in range(len(self.addresses)):
                index = i + 1
                address = self.addresses[i]['address']
                account = [index, address]
                for token in TOKENS_DICT.values():
                    token_balance = balances[i][token.name]
                    account.append(token_balance)
                if balances[i]['user_token'] != '':
                    user_token = balances[i]['user_token']
                    user_token_balance = user_token
                    account += [user_token_balance]
                accounts.append(account)
        except TypeError:
            utils.log_error(f'{log_process} | {balances[0][1]}')
            return []
        return accounts

    @staticmethod
    def _get_headers() -> list[str]:
        headers = ['index', 'address', 'user token']
        for token_name in TOKENS_DICT.keys():
            headers.insert(len(headers) - 1, token_name)
        return headers

    async def _create_csv(self, log_process: str):
        my_csv = MyCSV()
        status, result = my_csv.create_file(data=self.accounts, addition_to_filepath=self.network.name.lower())
        if status == -1:
            utils.log_error(f'{log_process} | {result}')
            return False
        else:
            utils.log_info(f'{log_process} | {result}')
            return True
