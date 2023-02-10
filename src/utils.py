"""Module for utility functions."""

import logging
import os
import sys
from time import time
from typing import Any, Callable

LOG_PATH = os.path.join(os.path.dirname(__file__), "../logs/")


def init_logger(file_name: str) -> None:
    log_file_path = os.path.join(LOG_PATH, file_name)
    if os.path.exists(log_file_path):
        os.remove(log_file_path)
    else:
        os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
    log_formatter = logging.Formatter("%(asctime)s:%(levelname)s: %(message)s")
    log_formatter.datefmt = "%Y-%m-%d %H:%M:%S"

    log_handler = logging.FileHandler(log_file_path)
    log_handler.suffix = "%Y%m%d"
    log_handler.setFormatter(log_formatter)
    log_handler.setLevel(logging.INFO)

    std_log_handler = logging.StreamHandler(sys.stdout)
    std_log_handler.suffix = "%Y%m%d"
    std_log_handler.setFormatter(log_formatter)
    std_log_handler.setLevel(logging.DEBUG)

    logger = logging.getLogger()
    logger.addHandler(std_log_handler)
    logger.addHandler(log_handler)
    logger.setLevel(logging.DEBUG)

    # Set library logging level to error
    for key in logging.Logger.manager.loggerDict:
        logging.getLogger(key).setLevel(logging.ERROR)

    logging.info(f"Logging file path: {os.path.abspath(log_file_path)}")
    logging.info("")


def timer_decorator(func: Callable) -> Callable:
    """Decorator that prints the time it took to execute a function."""

    def wrapper_function(*args, **kwargs) -> Any:
        """Wrapper function that prints the time it took to execute a function.

        Returns:
            Any: the result of the function
        """
        t1 = time()
        result = func(*args, **kwargs)
        t2 = time()
        logging.info(
            f"Method {func.__name__!r} of module {func.__module__!r} executed in {t2 - t1:.4f} seconds."
        )
        return result

    return wrapper_function
