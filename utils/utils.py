# types
from typing import Optional

# libraries
from functools import wraps

# lib
from lib import my_logger


def handle_system_message(message: str, logger_level: my_logger.Level) -> None:
    if logger_level == my_logger.DEB:
        my_logger.logger.debug(message)
    elif logger_level == my_logger.INF:
        my_logger.logger.info(message)
    elif logger_level == my_logger.WAR:
        my_logger.logger.warn(message)
    elif logger_level == my_logger.ERR:
        my_logger.logger.error(message)
    elif logger_level == my_logger.FAT:
        my_logger.logger.fatal(message)
    else:
        my_logger.logger.debug(f'No such a level {logger_level.name} in logger | message: {message}')


def log_info(message: str) -> None:
    handle_system_message(message=message, logger_level=my_logger.INF)


def log_debug(message: str) -> None:
    handle_system_message(message=message, logger_level=my_logger.DEB)


def log_warn(message: str) -> None:
    handle_system_message(message=message, logger_level=my_logger.WAR)


def log_error(message: str) -> None:
    handle_system_message(message=message, logger_level=my_logger.ERR)


def log_fatal(message: str) -> None:
    handle_system_message(message=message, logger_level=my_logger.FAT)


def log_function(level: my_logger.Level, process: Optional[str] = None):
    def decorator(func):
        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            log_process, func_name = args[0] if args else kwargs.get('log_process', ''), func.__name__
            if process is not None:
                if process == '':
                    message_b = f'{log_process} | Running...'
                    message_a = f'{log_process} | Done!'
                else:
                    message_b = f'{log_process} | {process} | Running...'
                    message_a = f'{log_process} | {process} | Done!'
            else:
                message_b = f'{log_process} | {func_name} | Running...'
                message_a = f'{log_process} | {func_name} | Done!'
            handle_system_message(message=message_b, logger_level=level)
            result = await func(self, *args, **kwargs)
            if result is not False:
                handle_system_message(message=message_a, logger_level=level)
            return result
        return wrapper
    return decorator


def create_options_table(options: list[str], values_in_row: int = 5) -> str:
    values = options.copy()
    max_len_item = len(max(values, key=len))
    for i in range(len(values)):
        values[i] += ' ' * (max_len_item - len(values[i]))
    separator = ' | '
    starter = '| '
    finisher = ' |'
    len_line = len(separator) * (len(values[:values_in_row]) - 1) + len(finisher) + len(starter) + max_len_item * len(values[:values_in_row])
    line = '-' * len_line
    start_line = line + '\n| '
    finish_line = '\n' + line
    options_table = start_line
    for i in range(1, len(values) + 1):
        index = i - 1
        options_table += values[index]
        if i % values_in_row <= values_in_row-1:
            options_table += separator
        if i % values_in_row == 0:
            options_table += '\n' + starter
    if len(values) % values_in_row == 0 and len(values) >= values_in_row:
        options_table = options_table[:-len('\n' + starter)]
    options_table += finish_line
    return options_table


def create_options_list_with_numbers(options: list[str]) -> str:
    options_list = ''
    i = 1
    for option in options:
        options_list += f'[{i}] {option}\n'
        i += 1
    options_list = options_list[:-2]
    return options_list
