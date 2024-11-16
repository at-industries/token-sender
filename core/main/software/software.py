# types
from typing import Optional, Union

# libraries
import random
import asyncio

# lib
from lib import my_logger as logger
from lib.my_web3.utils import get_anonymous_string

# core
from core.models import Data
from core.models.value import DEFAULT, Value
from core.modules.module import Module
from core.models.account import Account
from core.models.command import Command
from core.db import table_sessions as db
from core.models.thread import Thread, Session

# utils
from utils import utils


class Software:
    process = 'SOFTWARE'

    def __init__(self, soft_data: Data, accounts: list[Account], n_retries: int):
        self.soft_data = soft_data
        self.accounts = accounts
        self.sessions = []
        self.threads = {}
        self.n_retries = n_retries
        self.project_name = self.soft_data.project_name

    async def __aenter__(self, ):
        self.welcome(self.process)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.goodbye(self.process)

    def welcome(self, log_process: str) -> None:
        utils.log_info(f'{log_process} | {self.project_name} has been started!')

    def goodbye(self, log_process: str) -> None:
        utils.log_info(f'{log_process} | {self.project_name} has been finished!')

    async def start(self, index: Optional[int] = None) -> None:
        if not await self.load_sessions(self.process, index=index):
            return
        if not await self.create_threads(self.process):
            return
        if not await self.run_threads(self.process):
            return

    async def load_sessions(self, log_process: str, index: Optional[int] = None) -> bool:
        sessions = await self._get_sessions(log_process=log_process, index=index)
        if not sessions:
            return False
        else:
            self.sessions = sessions
            return True

    async def _get_sessions(self, log_process: str, index: Optional[int] = None) -> list[Session]:
        if index is not None:
            return [db.get_session(index=index)]
        else:
            return db.get_all_sessions()

    async def create_threads(self, log_process: str) -> bool:
        threads = await self._create_threads(log_process=log_process)
        if not threads:
            return False
        else:
            self.threads = threads
            return True

    async def _create_threads(self, log_process: str, ) -> list[Thread]:
        threads = []
        for session in self.sessions:
            account_thread = self.accounts[session.index].Main.thread
            if any(t_thread.index == account_thread for t_thread in threads):
                for thread in threads:
                    if thread.index == account_thread:
                        thread.sessions.append(session)
                        break
            else:
                threads.append(Thread(index=account_thread, sessions=[session]))
        return threads

    async def run_threads(self, log_process: str) -> bool:
        max_thread_number = len(str(max(thread.index for thread in self.threads)))
        accounts_active = self._get_accounts_active()
        tasks = []
        for thread in self.threads:
            tasks.append(
                asyncio.create_task(
                    self.run_thread(
                        log_process=f'{log_process} | THREAD: {str(thread.index).zfill(max_thread_number)}',
                        thread=thread,
                    )
                )
            )
        await asyncio.wait(tasks)
        n_accounts_executed = 0
        for task in tasks:
            n_accounts_executed += task.result()
        utils.log_info(f'{log_process} | Accounts ({n_accounts_executed}/{len(accounts_active)}) were executed!')
        return True

    def _get_accounts_active(self, ) -> list[Account]:
        accounts = []
        for account in self.accounts:
            for session in self.sessions:
                if account.index == session.index:
                    accounts.append(account)
        return accounts

    async def run_thread(self, log_process: str, thread: Thread) -> int:
        await asyncio.sleep(1)
        n_accounts_executed = 0
        for session in thread.sessions:
            address = get_anonymous_string(self.accounts[session.index].Main.address)
            if await self.run_sessions(f'{log_process} | add: {address}', session):
                n_accounts_executed += 1
            else:
                break
        return n_accounts_executed

    async def run_sessions(self, log_process: str, session: Session) -> bool:
        for i in range(1, self.n_retries + 1):
            session = db.get_session(index=session.index)
            utils.log_debug(f'{log_process} | RETRIES | {i}/{self.n_retries}')
            if await self.run_session(log_process, session):
                return True
            else:
                if i != self.n_retries:
                    await asyncio.sleep(
                        random.randint(self.soft_data.time_sleep.long_min, self.soft_data.time_sleep.long_max)
                    )
        return False

    @utils.log_function(level=logger.INF, process='')
    async def run_session(self, log_process: str, session: Session) -> bool:
        t_index = session.get_t_index()
        if t_index != -1:
            for command in session.commands[t_index:]:
                if not await self.run_command(log_process, session, command, (command.index == t_index)):
                    utils.log_error(f'{log_process} | Has been stopped!')
                    return False
        db.delete_session(session=session)
        return True

    async def run_command(self, log_process: str, session: Session, command: Command, start: bool) -> bool:

        # update
        session: Session = db.get_session(index=session.index)
        command: Command = session.commands[command.index]
        account: Account = self.accounts[session.index]

        module: Module = account.get_field(field_name=command.module)
        display = await module.get_display(account=account, command=command)
        display_b, display_a = await module.get_display_software(account=account, command=command, start=start)
        if display_b != DEFAULT:
            utils.log_info(f'{log_process} | {display_b} | Running...')
        if not await module.invoke(command.function, f'{log_process} | {display}', session, command, account):
            return False
        if display_a != DEFAULT:
            utils.log_info(f'{log_process} | {display_a} | Done!')
        if not await self.sleep(account, session, command, display_a):
            return False
        return True

    async def sleep(self, account: Account, session: Session, command: Command, display_a: Union[str, Value]) -> bool:
        if display_a == DEFAULT:
            time_min = self.soft_data.time_sleep.short_min
            time_max = self.soft_data.time_sleep.short_max
        else:
            if command.index == len(session.commands) - 1:
                return True
            else:
                if account.Main.Sleep == 1:
                    time_min = account.Sleep.min
                    time_max = account.Sleep.max
                else:
                    time_min = self.soft_data.time_sleep.long_min
                    time_max = self.soft_data.time_sleep.long_max
        await asyncio.sleep(random.randint(time_min, time_max))
        return True
