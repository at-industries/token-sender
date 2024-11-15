class Value:
    def __init__(self, name: str):
        self.name = name

    def __str__(self) -> str:
        return (
            f"Value("
            f"name={repr(self.name)}"
            f")"
        )

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other) -> bool:
        if isinstance(other, Value):
            return self.name == other.name
        return False


OK = Value(
    name='OK',
)
TRUE = Value(
    name='TRUE',
)
FALSE = Value(
    name='FALSE',
)
DEFAULT = Value(
    name='DEFAULT',
)
VALUES_DICT = {
    OK.name: OK,
    TRUE.name: TRUE,
    FALSE.name: FALSE,
    DEFAULT.name: DEFAULT,
}
VALUES_LIST = list(VALUES_DICT.values())
VALUES_NAMES_LIST = list(VALUES_DICT.keys())
