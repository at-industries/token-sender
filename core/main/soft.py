# libraries
import time

# data
from data.constants import *

# core
from core.models import TimeSleep, Data
from core.main.launcher.launcher import Launcher
from core.modules import MODULES_LIST, MODULES_DICT


TIME_SLEEP = TimeSleep(
    long_min=TIME_SLEEP_LONG_MIN, long_max=TIME_SLEEP_LONG_MAX,
    short_min=TIME_SLEEP_SHORT_MIN, short_max=TIME_SLEEP_SHORT_MAX,
)
DATA = Data(
    time_sleep=TIME_SLEEP,
    project_name=PROJECT_NAME,
    filename_settings=FILENAME_SETTINGS,
    modules_list=MODULES_LIST, modules_dict=MODULES_DICT,
)


class Soft:
    def __init__(self, ):
        self.data = DATA
        self.project_name = self.data.project_name

    async def __aenter__(self, ):
        self.welcome()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.goodbye()

    def welcome(self, ) -> None:
        print(f'Welcome to {self.project_name}!')
        time.sleep(1)

    def goodbye(self, ) -> None:
        return

    async def start(self, ) -> None:
        async with Launcher(self.data) as launcher:
            await launcher.start()
