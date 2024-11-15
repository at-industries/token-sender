class TxType:
    def __init__(self, name: str,):
        self.name = name


LEGACY = TxType(
    name='Legacy',
)
EIP_1559 = TxType(
    name='EIP-1559',
)
TX_TYPES_DICT = {
    LEGACY.name: LEGACY,
    EIP_1559.name: EIP_1559,
}
TX_TYPES_LIST = list(TX_TYPES_DICT.values())
TX_TYPES_NAMES_LIST = list(TX_TYPES_DICT.keys())
