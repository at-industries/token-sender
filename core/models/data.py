# .
from .timesleep import TimeSleep

# types
from typing import Type

# core
from core.modules import Module


class Data:
    def __init__(
            self,
            project_name: str,
            filename_settings,
            time_sleep: TimeSleep,
            modules_list: list[Type[Module]],
            modules_dict: dict[str, Type[Module]],
    ):
        self.project_name = project_name
        self.filename_settings = filename_settings
        self.time_sleep = time_sleep
        self.modules_list = modules_list
        self.modules_dict = modules_dict
