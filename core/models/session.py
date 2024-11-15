# .
from .value import DEFAULT
from .command import Command


class Session:
    def __init__(self, index: int = None, commands: list[Command] = None):
        self.index = index
        self.commands = commands

    def get_t_index(self, ) -> int:
        t_index = -1
        for i in range(len(self.commands)):
            if self.commands[i].status == DEFAULT:
                t_index = i
                break
        return t_index
