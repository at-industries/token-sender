from .core import setup_logger
from .constants import *
from .levels import *


logger = setup_logger(
    directory=DIRECTORY,
    datefmt=DATETIME,
    format=FORMAT,
)
