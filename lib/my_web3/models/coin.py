class Coin:
    def __init__(self, name: str, n_decimals: int):
        self.name = name
        self.n_decimals = n_decimals


AVAX = Coin(
    name='AVAX',
    n_decimals=18,
)
BNB = Coin(
    name='BNB',
    n_decimals=18,
)
CELO = Coin(
    name='CELO',
    n_decimals=18,
)
ETH = Coin(
    name='ETH',
    n_decimals=18,
)
FTM = Coin(
    name='FTM',
    n_decimals=18,
)
GLMR = Coin(
    name='GLMR',
    n_decimals=18,
)
MATIC = Coin(
    name='MATIC',
    n_decimals=18,
)
MOVR = Coin(
    name='MOVR',
    n_decimals=18,
)
COINS_DICT = {
    AVAX.name: AVAX,
    BNB.name: BNB,
    CELO.name: CELO,
    ETH.name: ETH,
    FTM.name: FTM,
    GLMR.name: GLMR,
    MATIC.name: MATIC,
    MOVR.name: MOVR,
}
COINS_LIST = list(COINS_DICT.values())
COINS_NAMES_LIST = list(COINS_DICT.keys())
