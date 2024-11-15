# .
from .value import DEFAULT

# types
from typing import Any


class Command:
    def __init__(
            self,
            index: Any = DEFAULT,
            module: Any = DEFAULT,
            function: Any = DEFAULT,
            status: Any = DEFAULT,
            value: Any = DEFAULT,
            info: Any = DEFAULT,
            extra: Any = DEFAULT,
    ):
        self.index = index
        self.module = module
        self.function = function
        self.status = status
        self.value = value
        self.info = info
        self.extra = extra

    def __str__(self, ) -> str:
        return (
            f"Command("
            f"index={repr(self.index)}, "
            f"module={repr(self.module)}, "
            f"function={repr(self.function)}, "
            f"status={repr(self.status)}, "
            f"value={repr(self.value)}, "
            f"info={repr(self.info)}, "
            f"extra={repr(self.extra)}"
            f")"
        )

    def __repr__(self, ) -> str:
        return self.__str__()
