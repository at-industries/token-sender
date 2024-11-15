from typing import Tuple, Union
from openpyxl.worksheet.protection import SheetProtection

import os
import inspect
import openpyxl
import pandas as pd
from pandas import DataFrame

from .models.sheet import Sheet


class MyExcel:
    def __init__(self, filename: str):
        self.filename = filename

    def is_file_exists(self, ) -> Tuple[int, Union[bool, Exception]]:
        log_process = f'{inspect.currentframe().f_code.co_name}'
        try:
            if os.path.isfile(self.filename):
                return 0, True
            else:
                return 0, False
        except Exception as e:
            return -1, Exception(f'{log_process} | {e}')

    def is_table_empty(self, ) -> Tuple[int, Union[bool, Exception]]:
        log_process = f'{inspect.currentframe().f_code.co_name}'
        try:
            sheets = pd.read_excel(self.filename, sheet_name=None)
            for sheet_name, df in sheets.items():
                if df.shape[0] > 0 and not df.iloc[1:].dropna(how='all').empty:
                    return 0, False
            return 0, True
        except Exception as e:
            return -1, Exception(f'{log_process} | {e}')

    def create_file(self, sheets: list[Sheet]) -> Tuple[int, Union[None, Exception]]:
        log_process = f'{inspect.currentframe().f_code.co_name}'
        try:
            with pd.ExcelWriter(self.filename, mode='w', engine='openpyxl') as writer:
                for sheet in sheets:
                    if sheet.view:
                        df = pd.DataFrame(columns=sheet.headers)
                        df.to_excel(writer, index=False, sheet_name=sheet.name)
            return 0, None
        except Exception as e:
            return -1, Exception(f'{log_process} | {e}')

    def get_sheet_as_dataframe(self, sheet_name: str) -> Tuple[int, Union[DataFrame, Exception]]:
        log_process = f'{inspect.currentframe().f_code.co_name}'
        try:
            return 0, pd.read_excel(self.filename, sheet_name=sheet_name)
        except Exception as e:
            return -1, Exception(f'{log_process} | {e}')

    def check_headers_for_sheet(self, sheet_name: str, headers: list[str]) -> Tuple[int, Union[bool, Exception]]:
        log_process = f'{inspect.currentframe().f_code.co_name}'
        try:
            status, result = self.get_sheet_as_dataframe(sheet_name=sheet_name)
            if status == 0:
                df = DataFrame(result)
                if list(df.columns) != headers:
                    return 0, False
                else:
                    return 0, True
            else:
                return -1, Exception(f'{log_process} | {result}')
        except Exception as e:
            return -1, Exception(f'{log_process} | {e}')

    def check_headers_for_sheets(self, sheets: list[Sheet]) -> Tuple[int, Union[bool, Exception]]:
        log_process = f'{inspect.currentframe().f_code.co_name}'
        try:
            for sheet in sheets:
                status, result = self.check_headers_for_sheet(sheet_name=sheet.name, headers=sheet.headers)
                if status == 0:
                    if not result:
                        return 0, False
                else:
                    return -1, Exception(f'{log_process} | {result}')
            return 0, True
        except Exception as e:
            return -1, Exception(f'{log_process} | {e}')

    def protect_sheet(self, sheet: Sheet) -> Tuple[int, Union[None, Exception]]:
        log_process = f'{inspect.currentframe().f_code.co_name}'
        try:
            workbook = openpyxl.load_workbook(self.filename)
            worksheet = workbook[sheet.name]
            worksheet.protection = SheetProtection(
                sheet=True,
                objects=True,
                scenarios=True,
                formatCells=False,
                formatColumns=False,
                formatRows=False,
                selectLockedCells=False,
                selectUnlockedCells=False,
            )
            workbook.save(self.filename)
            return 0, None
        except Exception as e:
            return -1, Exception(f'{log_process} | {e}')

    def get_table_as_dict(self, ) -> Tuple[int, Union[dict, Exception]]:
        log_process = f'{inspect.currentframe().f_code.co_name}'
        try:
            sheets = pd.read_excel(self.filename, sheet_name=None)
            max_rows = max(df.shape[0] for df in sheets.values())
            table_dict = {}
            for sheet_name, df in sheets.items():
                df = df.where(pd.notnull(df), None)
                if df.shape[0] < max_rows:
                    additional_rows = max_rows - df.shape[0]
                    empty_df = pd.DataFrame(
                        data=None,
                        columns=df.columns,
                        index=range(additional_rows),
                    )
                    df = pd.concat([df, empty_df], ignore_index=True)
                df = df.apply(lambda column: column.map(lambda x: None if pd.isna(x) else x))
                table_dict[sheet_name] = df.to_dict(orient='records')
            return 0, table_dict
        except Exception as e:
            return -1, Exception(f'{log_process} | {e}')
