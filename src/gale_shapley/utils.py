"""Module for utility functions."""

import logging
from pathlib import Path
from time import time
from typing import Callable, TypeVar

from rich.logging import RichHandler
from typing_extensions import (
    ParamSpec,  # need typing_extensions for Python < 3.10; Paramspec is new in Python 3.10, see https://www.python.org/dev/peps/pep-0612/
)

from gale_shapley.config import YAMLConfig

# Define TypeVars and ParamSpecs
R = TypeVar("R")
P = ParamSpec("P")
LOG_PATH: Path = Path(__file__).parents[2] / "logs"


# Define function to initialize the logger
def init_logger(file_name: str) -> None:
    """Initialize the logger.

    Args:
        file_name (str): The name of the log file.
    """
    # Set the log file path and create it if it does not exist
    log_file: Path = LOG_PATH / file_name
    log_file.unlink(missing_ok=True)
    log_file.touch()

    # Set the log formatter and handler levels for the log file
    log_formatter = logging.Formatter("%(asctime)s:%(levelname)s: %(message)s")
    log_formatter.datefmt = "%Y-%m-%d %H:%M:%S"
    log_handler = logging.FileHandler(str(log_file))
    log_handler.setFormatter(log_formatter)
    log_handler.setLevel(logging.INFO)

    # Set the log formatter and handler levels for the standard output
    std_log_formatter = logging.Formatter("%(message)s")
    std_log_formatter.datefmt = "%H:%M:%S"
    std_log_handler = RichHandler()
    std_log_handler.setFormatter(std_log_formatter)

    # Add handlers to the logger and set the logging level
    logger = logging.getLogger()
    logger.addHandler(std_log_handler)
    logger.addHandler(log_handler)
    logger.setLevel(logging.DEBUG)

    # Set library logging level to error
    for key in logging.Logger.manager.loggerDict:
        logging.getLogger(key).setLevel(logging.ERROR)

    # Log the path to log file
    logging.info(f"Path to log file: {log_file.resolve()}")


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

        Args:
            *args (P.args): Positional arguments for the function.
            **kwargs (P.kwargs): Keyword arguments for the function.

        Returns:
            R: The result of the function.
        """
        # Get the start time and execute the function
        t1: float = time()
        result: R = func(*args, **kwargs)

        # Get the end time and calculate the elapsed time
        t2: float = time()
        elapsed_time = t2 - t1

        # Log the execution time and return the result of the function
        logging.info(
            f"Method {func.__name__!r} of module {func.__module__!r} executed in {elapsed_time:.4f} seconds"
        )
        return result

    return wrapper
