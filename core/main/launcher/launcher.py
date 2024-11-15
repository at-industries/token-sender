# libraries
import time
import inspect

# lib
from lib import my_logger as logger
from lib.my_excel import MyExcel, Sheet

# core
from core.models import Data
from core.db import table_sessions as db
from core.main.launcher.multiple import Multiple
from core.main.software.checker import Checker

# utils
from utils import utils


class Launcher:
    process = 'LAUNCHER'

    def __init__(self, soft_data: Data):
        self.soft_data = soft_data
        self.sheets = self._fetch_sheets()
        self.project_name = self.soft_data.project_name
        self.filename_settings = self.soft_data.filename_settings
        self.excel = MyExcel(filename=self.filename_settings)

    async def __aenter__(self, ):
        self.welcome(self.process)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.goodbye(self.process)

    def welcome(self, log_process: str) -> None:
        utils.log_info(f'{log_process} | {self.project_name} has been launched!')

    def goodbye(self, log_process: str) -> None:
        utils.log_info(f'{log_process} | {self.project_name} has been finished!')

    async def start(self, ) -> None:
        if not await self.check(self.process):
            return
        if not await self.start_choice(self.process):
            return

    async def check(self, log_process: str) -> bool:
        if not await self.check_file(f'{log_process} | CHECK_0'):
            return False
        if not await self.check_sessions(f'{log_process} | CHECK_1'):
            return False
        return True

    @utils.log_function(level=logger.INF, process='')
    async def check_file(self, log_process: str) -> bool:
        if not await self._check_file_exists(f'{log_process} | {inspect.currentframe().f_code.co_name}'):
            return False
        if not await self._check_file_sheets(f'{log_process} | {inspect.currentframe().f_code.co_name}'):
            return False
        return True

    @utils.log_function(level=logger.DEB)
    async def _check_file_exists(self, log_process: str) -> bool:
        file_exists, msg = self.excel.is_file_exists()
        if file_exists == -1:
            utils.log_error(f'{log_process} | {inspect.currentframe().f_code.co_name} | {msg}')
            return False
        if not msg:
            utils.log_error(f'{log_process} | Filename {self.filename_settings} does not exist!')
            _ = await self._handle_file_not_exists(f'{log_process} | {inspect.currentframe().f_code.co_name}')
            return False
        return True

    @utils.log_function(level=logger.DEB)
    async def _handle_file_not_exists(self, log_process: str) -> bool:
        if not await self._create_file(f'{log_process} | {inspect.currentframe().f_code.co_name}'):
            return False
        if not await self._protect_sheets(f'{log_process} | {inspect.currentframe().f_code.co_name}'):
            return False
        return True

    @utils.log_function(level=logger.DEB)
    async def _create_file(self, log_process: str) -> bool:
        result, message = self.excel.create_file(sheets=self.sheets)
        if result == -1:
            utils.log_error(f'{log_process} | {inspect.currentframe().f_code.co_name} | {message}')
            return False
        return True

    @utils.log_function(level=logger.DEB)
    async def _protect_sheets(self, log_process: str) -> bool:
        for sheet in self.sheets:
            if sheet.protected:
                if not await self._protect_sheet(f'{log_process} | {inspect.currentframe().f_code.co_name}', sheet):
                    return False
        return True

    @utils.log_function(level=logger.DEB)
    async def _protect_sheet(self, log_process: str, sheet: Sheet) -> bool:
        result, message = self.excel.protect_sheet(sheet=sheet)
        if result == -1:
            utils.log_error(f'{log_process} | {inspect.currentframe().f_code.co_name} | {message}')
            return False
        return True

    @utils.log_function(level=logger.DEB)
    async def _check_file_sheets(self, log_process: str) -> bool:
        if not await self._check_file_sheets_headers(f'{log_process} | {inspect.currentframe().f_code.co_name}'):
            return False
        return True

    @utils.log_function(level=logger.DEB)
    async def _check_file_sheets_headers(self, log_process: str) -> bool:
        for sheet in self.sheets:
            if not await self._check_file_sheet_headers(
                    log_process=f'{log_process} | {inspect.currentframe().f_code.co_name}', sheet=sheet,
            ):
                return False
        return True

    @utils.log_function(level=logger.DEB)
    async def _check_file_sheet_headers(self, log_process: str, sheet: Sheet) -> bool:
        status, result = self.excel.check_headers_for_sheet(sheet_name=sheet.name, headers=sheet.headers)
        if status == -1:
            utils.log_error(f'{log_process} | {inspect.currentframe().f_code.co_name} | {result}')
            return False
        if not result:
            utils.log_error(f'{log_process} | Wrong headers for the sheet {sheet.name}!')
            return False
        return True

    @utils.log_function(level=logger.INF, process='')
    async def check_sessions(self, log_process: str) -> bool:
        if not db.get_all_sessions():
            return True
        async with Multiple(log_process, self.soft_data, self.excel) as launcher_multiple:
            await launcher_multiple.finish()
        return False

    async def start_choice(self, log_process: str) -> bool:
        time.sleep(1)
        while True:
            answer = input(
                f'What do you want to do?\n'
                f'[1] Launch multiple modules (selected in {self.filename_settings})\n'
                f'[2] Launch checker\n'
                f'[3] Close\n'
            )
            if answer == '1':
                async with Multiple(log_process, self.soft_data, self.excel) as launcher_multiple:
                    await launcher_multiple.start()
                break
            elif answer == '2':
                async with Checker(log_process, self.soft_data, self.excel) as launcher_checker:
                    await launcher_checker.start()
                break
            elif answer == '3':
                break
            else:
                print(f'No such an answer!')
        return True

    def _fetch_sheets(self, ) -> list[Sheet]:
        sheets = []
        for module_type in self.soft_data.modules_list:
            module = module_type()
            if module.sheet.view:
                sheets.append(module.sheet)
        return sheets
