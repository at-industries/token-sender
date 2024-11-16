# types
from typing import Union

# libraries
import time
import inspect

# lib
from lib.my_excel import MyExcel
from lib import my_logger as logger
from lib.my_web3.utils import get_anonymous_string

# core
from core.models import Data
from core.models.value import DEFAULT
from core.modules.module import Module
from core.models.account import Account
from core.models.session import Session
from core.db import table_sessions as db
from core.main.software.software import Software

# utils
from utils import utils


class Multiple:
    process = 'MULTIPLE'

    def __init__(self, log_process: str, soft_data: Data, excel: MyExcel):
        self.process = f'{log_process} | {self.process}'
        self.soft_data = soft_data
        self.excel = excel
        self.table = {}
        self.accounts = []
        self.sessions = []

    async def __aenter__(self, ):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        return

    async def start(self, ) -> None:
        if not await self.load_table(self.process):
            return
        if not await self.load_accounts(self.process):
            return
        if not await self.check(self.process):
            return
        if not await self.create_sessions(self.process):
            return
        if not await self.show_sessions(self.process, False):
            return
        if not await self.start_choice(self.process):
            return

    async def check(self, log_process: str) -> bool:
        if not await self.check_accounts(f'{log_process} | CHECK_0'):
            return False
        return True

    async def finish(self, ) -> None:
        if not await self.load_table(self.process):
            return
        if not await self.load_accounts(self.process):
            return
        if not await self.show_sessions(self.process, True):
            return
        if not await self.finish_choice(self.process):
            return

    @utils.log_function(level=logger.DEB)
    async def load_table(self, log_process: str) -> bool:
        table = await self._get_table(f'{log_process} | {inspect.currentframe().f_code.co_name}')
        if not table:
            return False
        else:
            self.table = table
            return True

    @utils.log_function(level=logger.DEB)
    async def _get_table(self, log_process: str) -> Union[bool, dict]:
        status, result = self.excel.get_table_as_dict()
        if status == -1:
            utils.log_error(f'{log_process} | {inspect.currentframe().f_code.co_name} | {result}')
            return False
        return dict(result)

    @utils.log_function(level=logger.DEB)
    async def load_accounts(self, log_process: str) -> bool:
        if not await self._load_accounts_dicts(f'{log_process} | {inspect.currentframe().f_code.co_name}'):
            return False
        if not await self._load_accounts_objects(f'{log_process} | {inspect.currentframe().f_code.co_name}'):
            return False
        return True

    @utils.log_function(level=logger.DEB)
    async def _load_accounts_dicts(self, log_process: str) -> bool:
        accounts = await self._get_accounts_dicts(f'{log_process} | {inspect.currentframe().f_code.co_name}')
        if not accounts:
            return False
        else:
            self.accounts = accounts
            return True

    @utils.log_function(level=logger.DEB)
    async def _get_accounts_dicts(self, log_process: str) -> Union[bool, list[dict]]:
        accounts = []
        data = self.table
        for i in range(len(next(iter(data.values())))):
            account = {}
            for module_name, accounts_list in data.items():
                account[module_name] = accounts_list[i]
            accounts.append(account)
        return accounts

    @utils.log_function(level=logger.DEB)
    async def _load_accounts_objects(self, log_process: str) -> bool:
        accounts = await self._get_accounts_objects(f'{log_process} | {inspect.currentframe().f_code.co_name}')
        if not accounts:
            return False
        else:
            self.accounts = accounts
            return True

    @utils.log_function(level=logger.DEB)
    async def _get_accounts_objects(self, log_process: str) -> Union[bool, list[Account]]:
        accounts = [Account() for _ in range(len(self.accounts))]
        for i in range(len(accounts)):
            data = {}
            for module_name, module_type in self.soft_data.modules_dict.items():
                if module_type().sheet.view:
                    module = module_type().fill_data(data=self.accounts[i][module_name])
                    data[module_name] = module
            accounts[i].fill_data(data=data)
            accounts[i].index = i
        return accounts

    @utils.log_function(level=logger.INF, process='')
    async def check_accounts(self, log_process: str) -> bool:
        for module_name, module in self.soft_data.modules_dict.items():
            for account in self.accounts:
                if not await module().check(log_process, account):
                    return False
        return True

    @utils.log_function(level=logger.DEB)
    async def create_sessions(self, log_process: str) -> bool:
        sessions = await self._create_sessions(f'{log_process} | {inspect.currentframe().f_code.co_name}')
        if not sessions:
            return False
        else:
            self.sessions = sessions
            return True

    @utils.log_function(level=logger.DEB)
    async def _create_sessions(self, log_process: str) -> Union[bool, list[Session]]:
        sessions = [Session(index=i, commands=[]) for i in range(len(self.accounts))]
        for i in range(len(sessions)):
            account = self.accounts[i]
            for module_name, module_type in self.soft_data.modules_dict.items():
                if module_type().sheet.view:
                    if account.Main.get_field(module_name) == 1:
                        module: Module = account.get_field(module_name)
                        sessions[i].commands += await module.create_commands(log_process, account)
            for j in range(len(sessions[i].commands)):
                sessions[i].commands[j].index = j
        return [session for session in sessions if session.commands]

    async def show_sessions(self, log_process: str, from_db: bool) -> bool:
        sessions = await self._get_sessions(log_process=log_process, from_db=from_db)
        max_session_index = len(str(max(session.index for session in sessions)))
        for session in sessions:
            account = self.accounts[session.index]
            index = str(session.index).zfill(max_session_index)
            address = get_anonymous_string(account.Main.address)
            path = await self._create_path(
                log_process=f'{log_process} | {inspect.currentframe().f_code.co_name}', account=account, session=session,
            )
            utils.log_info(f'{log_process} | DISPLAY | index: {index} | add: {address} | path: {path}')
        return True

    async def _get_sessions(self, log_process: str, from_db: bool) -> list[Session]:
        if from_db:
            return db.get_all_sessions()
        else:
            return self.sessions

    async def _create_path(self, log_process: str, account: Account, session: Session) -> str:
        path = ''
        for command in session.commands:
            module = account.get_field(field_name=str(command.module))
            display = await module.get_display_launcher(account=account, command=command)
            if display != DEFAULT:
                if path == '':
                    path += f'{display}'
                else:
                    path += f' -> {display}'
        return path

    async def start_choice(self, log_process: str) -> bool:
        time.sleep(1)
        print(f'Software is ready to start! Do you want to start it? (yes/no)')
        while True:
            answer = input()
            if answer == 'yes':
                print(f'How many retries do you want to have? (integer number)')
                while True:
                    try:
                        n_retries = int(input())
                        if n_retries > 0:
                            for session in self.sessions:
                                if session.commands:
                                    db.add_session(session=session)
                            async with Software(self.soft_data, self.accounts, n_retries) as software:
                                await software.start()
                            break
                        else:
                            print(f'Retries must be greater than zero!')
                    except ValueError:
                        print(f'Retries must be integer!')
                break
            elif answer == 'no':
                break
            else:
                print(f'No such an answer! (yes/no)')
        return True

    async def finish_choice(self, log_process: str) -> bool:
        time.sleep(1)
        print('You have unfinished sessions! Do you want to finish them?                                   ')
        print('|----------------|-------------------------------------------------------------------------|')
        print('| Command:       | Function:                                                               |')
        print('|----------------|-------------------------------------------------------------------------|')
        print('| finish all     | finish all unfinished sessions                                          |')
        print('| delete all     | delete all unfinished sessions                                          |')
        print('| finish <index> | finish specific one (take <index> above), e.g: finish 13 OR finish 0013 |')
        print('| delete <index> | delete specific one (take <index> above), e.g: delete 13 OR delete 0013 |')
        print('| close          | close the software                                                      |')
        print('|----------------|-------------------------------------------------------------------------|')
        while True:
            answer = input()
            if answer == 'finish all':
                print(f'How many retries do you want to have? (integer number)')
                while True:
                    try:
                        n_retries = int(input())
                        if n_retries > 0:
                            async with Software(self.soft_data, self.accounts, n_retries) as software:
                                await software.start()
                            break
                        else:
                            print(f'Retries must be greater than zero!')
                    except ValueError:
                        print(f'Retries must be integer!')
                break
            elif answer == 'delete all':
                db.clear_database()
                print(f'All sessions were deleted! Restart the software to use it!')
                time.sleep(1)
                break
            elif ('finish ' in answer) and ('finish ' != answer):
                _, index = answer.split()
                try:
                    index = int(index)
                    if index in db.get_all_indexes():
                        print(f'How many retries do you want to have? (integer number)')
                        while True:
                            try:
                                n_retries = int(input())
                                if n_retries > 0:
                                    async with Software(self.soft_data, self.accounts, n_retries) as software:
                                        await software.start(index=index)
                                    break
                                else:
                                    print(f'Retries must be greater than zero!')
                            except ValueError:
                                print(f'Retries must be integer!')
                        break
                    else:
                        print(f'No such a session!')
                except ValueError:
                    print(f'Index must be integer!')
            elif ('delete ' in answer) and ('delete ' != answer):
                _, index = answer.split()
                try:
                    index = int(index)
                    if index in db.get_all_indexes():
                        db.delete_session_by_index(index=index)
                        print(f'Session was deleted! Restart the software to use it!')
                        time.sleep(1)
                        break
                    else:
                        print(f'No such a session!')
                except ValueError:
                    print(f'Index must be integer!')
            elif answer == 'close':
                break
            else:
                print(f'No such an answer!')
        return True
