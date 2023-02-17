"""Module for utility functions."""

import logging
import os
import sys
from time import time
from typing import Callable, TypeVar

from typing_extensions import (  # Paramspec is new in Python 3.10, see https://www.python.org/dev/peps/pep-0612/
    ParamSpec,
)

R = TypeVar("R")
P = ParamSpec("P")
LOG_PATH: str = os.path.join(os.path.dirname(__file__).split("src")[0], "logs/")


def init_logger(file_name: str) -> None:
    """Initialize the logger.

    Args:
        file_name (str): the name of the log file
    """
    log_file_path: str = os.path.join(LOG_PATH, file_name)
    if os.path.exists(log_file_path):
        os.remove(log_file_path)
    else:
        os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
    log_formatter = logging.Formatter("%(asctime)s:%(levelname)s: %(message)s")
    log_formatter.datefmt = "%Y-%m-%d %H:%M:%S"

    log_handler = logging.FileHandler(log_file_path)
    log_handler.setFormatter(log_formatter)
    log_handler.setLevel(logging.INFO)

    std_log_handler = logging.StreamHandler(sys.stdout)
    std_log_handler.setFormatter(log_formatter)
    std_log_handler.setLevel(logging.DEBUG)

    logger = logging.getLogger()
    logger.addHandler(std_log_handler)
    logger.addHandler(log_handler)
    logger.setLevel(logging.DEBUG)

    # Set library logging level to error
    for key in logging.Logger.manager.loggerDict:
        logging.getLogger(key).setLevel(logging.ERROR)

    logging.info(f"Path to log file: {os.path.abspath(log_file_path)}")
    logging.info("")


def timer_decorator(func: Callable[P, R]) -> Callable[P, R]:
    """Decorator that prints the time it took to execute a function."""

    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        """Wrapper function that prints the time it took to execute a function.

        Returns:
            Any: the result of the function
        """
        t1: float = time()
        result = func(*args, **kwargs)
        t2: float = time()
        logging.info(
            f"Method {func.__name__!r} of module {func.__module__!r} executed in {t2 - t1:.2f} seconds."
        )
        return result

    return wrapper
