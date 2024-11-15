from .coin import *
from .txtype import *

import random


class Network:
    def __init__(
            self,
            name: str, rpc: str,
            coin: Coin, chain_id: int, tx_type: TxType,
            step_withdraw_min: float, step_withdraw_max: float,
    ):
        self.name = name
        self.rpc = rpc
        self.coin = coin
        self.tx_type = tx_type
        self.chain_id = chain_id
        self.step_withdraw_min = step_withdraw_min
        self.step_withdraw_max = step_withdraw_max

    def get_step_withdraw(self, ) -> int:
        scale = 10 ** self.coin.n_decimals
        return random.randint(int(self.step_withdraw_min * scale), int(self.step_withdraw_max * scale))


ARBITRUM = Network(
    name='Arbitrum',
    rpc='https://arbitrum-one.public.blastapi.io',
    coin=ETH,
    chain_id=42161,
    tx_type=EIP_1559,
    step_withdraw_min=0.0000001,
    step_withdraw_max=0.0000001,
)
AVALANCHE = Network(
    name='Avalanche',
    rpc='https://ava-mainnet.public.blastapi.io/ext/bc/C/rpc',
    coin=AVAX,
    chain_id=43114,
    tx_type=EIP_1559,
    step_withdraw_min=0.0000001,
    step_withdraw_max=0.0000001,
)
BASE = Network(
    name='Base',
    rpc='https://base-mainnet.public.blastapi.io',
    coin=ETH,
    chain_id=8453,
    tx_type=EIP_1559,
    step_withdraw_min=0.0000001,
    step_withdraw_max=0.0000001,
)
BSC = Network(
    name='BSC',
    rpc='https://bsc-mainnet.public.blastapi.io',
    coin=BNB,
    chain_id=56,
    tx_type=EIP_1559,
    step_withdraw_min=0.0000001,
    step_withdraw_max=0.0000001,
)
CELO = Network(
    name='Celo',
    rpc='https://1rpc.io/celo',
    coin=CELO,
    chain_id=42220,
    tx_type=EIP_1559,
    step_withdraw_min=0.0000001,
    step_withdraw_max=0.0000001,
)
ETHEREUM = Network(
    name='Ethereum',
    rpc='https://eth-mainnet.public.blastapi.io',
    coin=ETH,
    chain_id=1,
    tx_type=EIP_1559,
    step_withdraw_min=0.0000001,
    step_withdraw_max=0.0000001,
)
FANTOM = Network(
    name='Fantom',
    rpc='https://fantom-mainnet.public.blastapi.io',
    coin=FTM,
    chain_id=250,
    tx_type=EIP_1559,
    step_withdraw_min=0.0000001,
    step_withdraw_max=0.0000001,
)
LINEA = Network(
    name='Linea',
    rpc='https://linea-mainnet.public.blastapi.io',
    coin=ETH,
    chain_id=59144,
    tx_type=EIP_1559,
    step_withdraw_min=0.0000001,
    step_withdraw_max=0.0000001,
)
MOONBEAM = Network(
    name='Moonbeam',
    rpc='https://moonbeam.public.blastapi.io',
    coin=GLMR,
    chain_id=1284,
    tx_type=EIP_1559,
    step_withdraw_min=0.0000001,
    step_withdraw_max=0.0000001,
)
MOONRIVER = Network(
    name='Moonriver',
    rpc='https://moonriver.public.blastapi.io',
    coin=MOVR,
    chain_id=1285,
    tx_type=EIP_1559,
    step_withdraw_min=0.0000001,
    step_withdraw_max=0.0000001,
)
OPTIMISM = Network(
    name='Optimism',
    rpc='https://optimism-mainnet.public.blastapi.io',
    coin=ETH,
    chain_id=10,
    tx_type=EIP_1559,
    step_withdraw_min=0.0000001,
    step_withdraw_max=0.0000001,
)
POLYGON = Network(
    name='Polygon',
    rpc='https://polygon-mainnet.public.blastapi.io',
    coin=MATIC,
    chain_id=137,
    tx_type=EIP_1559,
    step_withdraw_min=0.0000001,
    step_withdraw_max=0.0000001,
)
POLYGON_ZKEVM = Network(
    name='Polygon_zkEVM',
    rpc='https://polygon-zkevm-mainnet.public.blastapi.io',
    coin=ETH,
    chain_id=1101,
    tx_type=EIP_1559,
    step_withdraw_min=0.0000001,
    step_withdraw_max=0.0000001,
)
SCROLL = Network(
    name='Scroll',
    rpc='https://scroll-mainnet.public.blastapi.io',
    coin=ETH,
    chain_id=534352,
    tx_type=EIP_1559,
    step_withdraw_min=0.0000001,
    step_withdraw_max=0.0000001,
)
ZKSYNC = Network(
    name='zkSync',
    rpc='https://zksync-mainnet.public.blastapi.io',
    coin=ETH,
    chain_id=324,
    tx_type=LEGACY,
    step_withdraw_min=0.0000001,
    step_withdraw_max=0.0000001,
)
NETWORKS_DICT = {
    ARBITRUM.name: ARBITRUM,
    AVALANCHE.name: AVALANCHE,
    BASE.name: BASE,
    BSC.name: BSC,
    CELO.name: CELO,
    ETHEREUM.name: ETHEREUM,
    FANTOM.name: FANTOM,
    LINEA.name: LINEA,
    MOONBEAM.name: MOONBEAM,
    MOONRIVER.name: MOONRIVER,
    OPTIMISM.name: OPTIMISM,
    POLYGON.name: POLYGON,
    POLYGON_ZKEVM.name: POLYGON_ZKEVM,
    SCROLL.name: SCROLL,
    ZKSYNC.name: ZKSYNC,
}
NETWORKS_LIST = list(NETWORKS_DICT.values())
NETWORK_NAMES_LIST = list(NETWORKS_DICT.keys())
