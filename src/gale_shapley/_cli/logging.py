"""Logging utilities for the CLI."""

import logging
from collections.abc import Callable
from pathlib import Path
from time import time
from typing import Final, ParamSpec, TypeVar

from rich.logging import RichHandler

from gale_shapley._cli.config import YAMLConfig

R = TypeVar("R")
P = ParamSpec("P")
LOG_PATH: Final[Path] = Path(__file__).parents[3] / "logs"


def init_logger(file_name: str) -> None:
    """Initialize the logger.

    Args:
        file_name: The name of the log file.
    """
    log_file: Final[Path] = LOG_PATH / file_name
    log_file.unlink(missing_ok=True)
    log_file.touch()

    log_formatter = logging.Formatter("%(asctime)s:%(levelname)s: %(message)s")
    log_formatter.datefmt = "%Y-%m-%d %H:%M:%S"
    log_handler = logging.FileHandler(str(log_file))
    log_handler.setFormatter(log_formatter)
    log_handler.setLevel(logging.INFO)

    std_log_formatter = logging.Formatter("%(message)s")
    std_log_formatter.datefmt = "%H:%M:%S"
    std_log_handler = RichHandler()
    std_log_handler.setFormatter(std_log_formatter)

    logger = logging.getLogger()
    logger.addHandler(std_log_handler)
    logger.addHandler(log_handler)
    logger.setLevel(logging.DEBUG)

    for key in logging.Logger.manager.loggerDict:
        logging.getLogger(key).setLevel(logging.ERROR)

    logging.info(f"Path to log file: {log_file.resolve()}")


def log_config_info(config_input: YAMLConfig) -> None:
    """Log the information from the config file.

    Args:
        config_input: The parsed and validated config input object.
    """
    logging.info("Parsing config.yaml is complete.")
    logging.info(
        f"Proposer side name: {config_input.proposer_side_name}, Responder side name: {config_input.responder_side_name}"
    )
    match config_input.preference_type:
        case "random":
            logging.info(
                f"Number of proposers: {config_input.number_of_proposers}, Number of responders: {config_input.number_of_responders}"
            )
        case "input":
            logging.info(
                f"Number of proposers: {len(config_input.proposers)}, Number of responders: {len(config_input.responders)}"
            )
    logging.info(f"Preference type: {config_input.preference_type}")


def timer_decorator(func: Callable[P, R]) -> Callable[P, R]:
    """Decorator that logs the time it took to execute a function."""

    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        t1: Final[float] = time()
        result: R = func(*args, **kwargs)
        t2: Final[float] = time()
        elapsed_time: Final[float] = t2 - t1
        logging.info(f"Method {func.__name__!r} of module {func.__module__!r} executed in {elapsed_time:.4f} seconds")
        return result

    return wrapper
