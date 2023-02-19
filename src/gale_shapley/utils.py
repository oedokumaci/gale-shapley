"""Module for utility functions."""

import logging
import sys
from pathlib import Path
from time import time
from typing import Callable, TypeVar

from typing_extensions import (  # Paramspec is new in Python 3.10, see https://www.python.org/dev/peps/pep-0612/
    ParamSpec,
)

R = TypeVar("R")
P = ParamSpec("P")
LOG_PATH: Path = Path(__file__).parent.parent.parent / "logs"


def init_logger(file_name: str) -> None:
    """Initialize the logger.

    Args:
        file_name (str): the name of the log file
    """
    log_file: Path = LOG_PATH / file_name
    log_file.unlink(missing_ok=True)
    log_file.touch()
    log_formatter = logging.Formatter("%(asctime)s:%(levelname)s: %(message)s")
    log_formatter.datefmt = "%Y-%m-%d %H:%M:%S"

    log_handler = logging.FileHandler(str(log_file))
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

    logging.info(f"Path to log file: {str(log_file.resolve())}")


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
