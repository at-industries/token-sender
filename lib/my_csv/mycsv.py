# .
from .constants import DIRECTORY

# libraries
import csv
import datetime
import inspect
import os

# types
from typing import Union, Tuple, Optional


class MyCSV:
    def create_file(self, data: list[list], addition_to_filepath: Optional[str] = None) -> Tuple[int, Union[str, Exception]]:
        log_process = f'{inspect.currentframe().f_code.co_name}'
        filename = self._get_csv_filepath(addition_to_filepath)
        try:
            with open(filename, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(data)
                result = f'{log_process} | "{filename}", has been created!'
        except Exception as e:
            return -1, Exception(f'{log_process} | {e}')
        return 0, result

    def _get_csv_filepath(self, addition_to_filepath: Union[None, str] = '') -> str:
        if not addition_to_filepath:
            filename = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S.csv')
        else:
            filename = addition_to_filepath + '_' + datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S.csv')
        return os.path.join(DIRECTORY, filename)
