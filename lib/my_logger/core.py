import logging
import os
import datetime


def setup_logger(directory: str, format: str, datefmt: str) -> logging.Logger:
    create_log_directory(directory=directory)
    filepath = get_log_file_path(directory=directory)
    configure_file_logger(
        filepath=filepath,
        datefmt=datefmt,
        format=format,
    )
    console_handler = configure_console_logger(format=format)
    logger = logging.getLogger()
    logger.addHandler(console_handler)
    return logger


def create_log_directory(directory: str) -> None:
    if not os.path.exists(directory):
        os.makedirs(directory)


def get_log_file_path(directory: str) -> str:
    filename = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S.log')
    return os.path.join(directory, filename)


def configure_file_logger(filepath: str, format: str, datefmt: str, level=logging.DEBUG) -> None:
    logging.basicConfig(
        level=level,
        format=format,
        datefmt=datefmt,
        filename=filepath,
    )


def configure_console_logger(format: str) -> logging.StreamHandler:
    console_handler = logging.StreamHandler()
    console_handler.setLevel(
        # logging.DEBUG,
        logging.INFO,
    )
    console_formatter = logging.Formatter(format)
    console_handler.setFormatter(console_formatter)
    return console_handler
