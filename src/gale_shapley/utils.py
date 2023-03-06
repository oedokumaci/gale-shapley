"""Module for utility functions."""

import logging
import sys
from pathlib import Path
from time import time
from typing import Callable, TypeVar

from typing_extensions import (
    ParamSpec,  # need typing_extensions for Python < 3.10; Paramspec is new in Python 3.10, see https://www.python.org/dev/peps/pep-0612/
)

from gale_shapley.config_parser import YAMLConfig

R = TypeVar("R")
P = ParamSpec("P")
LOG_PATH: Path = Path(__file__).parents[2] / "logs"


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


def log_config_info(config_input: YAMLConfig) -> None:
    """Log the information from the config file.

    Args:
        config_input (YAMLConfig): The parsed and validated config input object
    """
    logging.info("Parsing config.yaml is complete.")
    logging.info(
        f"Proposer side name: {config_input.proposer_side_name}, Responder side name: {config_input.responder_side_name}"
    )
    if config_input.preference_type == "random":
        logging.info(
            f"Number of proposers: {config_input.number_of_proposers}, Number of responders: {config_input.number_of_responders}"
        )
    elif config_input.preference_type == "input":
        logging.info(
            f"Number of proposers: {len(config_input.proposers)}, Number of responders: {len(config_input.responders)}"
        )
    logging.info(f"Preference type: {config_input.preference_type}")


def timer_decorator(func: Callable[P, R]) -> Callable[P, R]:
    """Decorator that prints the time it took to execute a function."""

    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        """Wrapper function that prints the time it took to execute a function.

        Returns:
            Any: the result of the function
        """
        t1: float = time()
        result: R = func(*args, **kwargs)
        t2: float = time()
        logging.info(
            f"Method {func.__name__!r} of module {func.__module__!r} executed in {t2 - t1:.3f} seconds."
        )
        return result

    return wrapper
