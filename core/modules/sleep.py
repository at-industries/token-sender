# types
import asyncio
from typing import Any, Union, Tuple

# libraries
import inspect

# lib
from lib.my_excel import Sheet
from lib import my_logger as logger

# core
from core.modules.constants import (
    NAME_SLEEP,
)
from core.models.value import (
    OK,
    DEFAULT,
)
from core.models.value import Value
from core.modules.module import Module
from core.models.command import Command
from core.models.session import Session

# utils
from utils import utils


class Sleep(Module):
    start: int
    min: int
    max: int

    def __init__(self, ):
        self.name = NAME_SLEEP
        self.sheet = Sheet(
            name=self.name,
            view=True,
            protected=False,
            headers=self.get_headers(),
        )

    async def get_display(self, account: Any, command: Command) -> str:
        return f'{self.name}({command.value})'

    async def get_display_launcher(self, account: Any, command: Command) -> Union[str, Value]:
        display = await self.get_display(account=account, command=command)
        if command.function == self.sleep.__name__:
            return display
        else:
            return DEFAULT

    async def get_display_software(self, account: Any, command: Command, start: bool) -> Tuple[Union[str, Value], Union[str, Value]]:
        display = await self.get_display(account=account, command=command)
        if start:
            return display, display
        else:
            return display, display

    async def create_commands(self, log_process: str, account: Any) -> list[Command]:
        return [Command(module=self.name, function=self.sleep.__name__, value=self.start)]

    @utils.log_function(level=logger.DEB)
    async def sleep(self, log_process: str, session: Session, command: Command, account: Any) -> bool:
        log_process = f'{log_process} | {inspect.currentframe().f_code.co_name}'
        try:
            time = int(command.value)
            while True:
                if time <= 0:
                    command.status = OK
                    self.save_command(session, command)
                    return True
                else:
                    await asyncio.sleep(1)
                    time -= 1
                    command.value = time
                    self.save_command(session, command)
        except Exception as e:
            utils.log_error(f'{log_process} | {e}')
            return False
