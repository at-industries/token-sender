from .network import *


class Token:
    def __init__(self, name: str, decimals: int, addresses: dict[Network, str]):
        self.name = name
        self.decimals = decimals
        self.addresses = addresses


USDT = Token(
    name='USDT',
    decimals=6,
    addresses={
        ARBITRUM: '0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9',
        AVALANCHE: '0x9702230A8Ea53601f5cD2dc00fDBc13d4dF4A8c7',
        BASE: '0xfde4C96c8593536E31F229EA8f37b2ADa2699bb2',
        BSC: '0x55d398326f99059ff775485246999027b3197955',
        CELO: '0x48065fbBE25f71C9282ddf5e1cD6D6A887483D5e',
        ETHEREUM: '0xdac17f958d2ee523a2206206994597c13d831ec7',
        FANTOM: '0x049d68029688eabf473097a2fc38ef61633a3c7a',
        LINEA: '0xa219439258ca9da29e9cc4ce5596924745e12b93',
        MOONBEAM: '0xefaeee334f0fd1712f9a8cc375f427d9cdd40d73',
        MOONRIVER: '0xe936caa7f6d9f5c9e907111fcaf7c351c184cda7',
        OPTIMISM: '0x94b008aa00579c1307b0ef2c499ad98a8ce58e58',
        POLYGON: '0xc2132d05d31c914a87c6611c10748aeb04b58e8f',
        POLYGON_ZKEVM: '0x1e4a5963abfd975d8c9021ce480b42188849d41d',
        SCROLL: '0xf55BEC9cafDbE8730f096Aa55dad6D22d44099Df',
        ZKSYNC: '0x493257fD37EDB34451f62EDf8D2a0C418852bA4C',
    }
)
USDC = Token(
    name='USDC',
    decimals=6,
    addresses={
        ARBITRUM: '0xaf88d065e77c8cC2239327C5EDb3A432268e5831',
        AVALANCHE: '0xB97EF9Ef8734C71904D8002F8b6Bc66Dd9c48a6E',
        BASE: '0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913',
        BSC: '0x8ac76a51cc950d9822d68b83fe1ad97b32cd580d',
        CELO: '0xcebA9300f2b948710d2653dD7B07f33A8B32118C',
        ETHEREUM: '0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48',
        FANTOM: '0x04068DA6C83AFCFA0e13ba15A6696662335D5B75',
        LINEA: '0x176211869cA2b568f2A7D4EE941E073a821EE1ff',
        MOONBEAM: '0x818ec0a7fe18ff94269904fced6ae3dae6d6dc0b',
        MOONRIVER: '0xe3f5a90f9cb311505cd691a46596599aa1a0ad7d',
        OPTIMISM: '0x0b2C639c533813f4Aa9D7837CAf62653d097Ff85',
        POLYGON: '0x3c499c542cEF5E3811e1192ce70d8cC03d5c3359',
        POLYGON_ZKEVM: '0xa8ce8aee21bc2a48a5ef670afcc9274c7bbbc035',
        SCROLL: '0x06eFdBFf2a14a7c8E15944D1F4A48F9F95F663A4',
        ZKSYNC: '0x1d17CBcF0D6D143135aE902365D2E5e2A16538D4',
    }
)
USDCe = Token(
    name='USDC.e',
    decimals=6,
    addresses={
        ARBITRUM: '0xFF970A61A04b1cA14834A43f5dE4533eBDDB5CC8',
        AVALANCHE: '0xa7d7079b0fead91f3e65f86e8915cb59c1a4c664',
        BASE: '',
        BSC: '',
        CELO: '',
        ETHEREUM: '',
        FANTOM: '',
        LINEA: '',
        MOONBEAM: '',
        MOONRIVER: '0x748134b5f553f2bcbd78c6826de99a70274bdeb3',
        OPTIMISM: '0x7f5c764cbc14f9669b88837ca1490cca17c31607',
        POLYGON: '0x2791bca1f2de4661ed88a30c99a7a9449aa84174',
        POLYGON_ZKEVM: '',
        SCROLL: '',
        ZKSYNC: '0xa7d7079b0fead91f3e65f86e8915cb59c1a4c664',
    }
)

TOKENS_DICT = {
    USDC.name: USDC,
    USDCe.name: USDCe,
    USDT.name: USDT,
}
TOKENS_LIST = list(TOKENS_DICT.values())
TOKENS_NAMES_LIST = list(TOKENS_DICT.keys())
