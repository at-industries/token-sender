from .module import Module
from .main import Main
from .sleep import Sleep
from .send import Send
from .withdraw import Withdraw


MODULES_DICT = {
    Main().name: Main,
    Sleep().name: Sleep,
    Send().name: Send,
    Withdraw().name: Withdraw,
}
MODULES_LIST = list(MODULES_DICT.values())
MODULES_NAMES_LIST = list(MODULES_DICT.keys())
