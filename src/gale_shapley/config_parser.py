"""This module contains the schema for the config.yaml file and parses it when imported."""

import logging
import os.path

import yaml
from exceptions import ConfigError, TwoSidedMatchingError
from utils import init_logger

PREFERENCE_TYPES = ["random"]


def _parse_proposer_and_responder(config: dict) -> tuple[str, str]:
    """Parses the proposer and responder from the config.yaml file.

    Args:
        config (dict): loaded config.yaml file

    Raises:
        ConfigError:
        TwoSidedMatchingError:

    Returns:
        tuple[str, str]: parsed proposer and responder
    """
    logging.info("Parsing proposer and responder from config.yaml...")

    try:
        proposer_and_responder = config["proposer_and_responder"]
    except (KeyError, TypeError):
        raise ConfigError(
            "proposer_and_responder is not specified properly in config.yaml, see example_config.yaml for an example"
        )

    if not isinstance(proposer_and_responder, list):
        raise ConfigError(
            "proposer_and_responder should be specified as a list in config.yaml, see example_config.yaml for an example"
        )
    if len(set(proposer_and_responder)) != 2:
        raise TwoSidedMatchingError(set(proposer_and_responder))
    proposer, responder = proposer_and_responder

    if not isinstance(proposer, str):
        raise ConfigError(f"Proposer should be a string, {proposer} is not a string")
    if not isinstance(responder, str):
        raise ConfigError(f"Responder should be a string, {responder} is not a string")

    logging.info("Parsing complete.")
    return proposer, responder


def _parse_number_of_proposers_and_responders(config: dict) -> tuple[int, int]:
    """Parses the number of proposers and responders from the config.yaml file.

    Args:
        config (dict): loaded config.yaml file

    Raises:
        ConfigError:

    Returns:
        tuple[int, int]: parsed number of proposers and responders
    """
    logging.info("Parsing number of proposers and responders from config.yaml...")

    try:
        number_of_proposers = config["number_of_proposers"]
    except (KeyError, TypeError):
        raise ConfigError(
            "number_of_proposers is not specified properly in config.yaml, see example_config.yaml for an example"
        )
    if not isinstance(number_of_proposers, int):
        raise ConfigError(
            "number_of_proposers should be specified as an integer in config.yaml, see example_config.yaml for an example"
        )

    try:
        number_of_responders = config["number_of_responders"]
    except (KeyError, TypeError):
        raise ConfigError(
            "number_of_responders is not specified properly in config.yaml, see example_config.yaml for an example"
        )
    if not isinstance(number_of_responders, int):
        raise ConfigError(
            "number_of_responders should be specified as an integer in config.yaml, see example_config.yaml for an example"
        )

    logging.info("Parsing complete.")
    return number_of_proposers, number_of_responders


def _parse_preference_type(config: dict) -> str:
    """Parses the preference type from the config.yaml file.

    Args:
        config (dict): loaded config.yaml file

    Raises:
        ConfigError:

    Returns:
        str: parsed preference type
    """
    logging.info("Parsing preference type from config.yaml...")

    try:
        preference_type = config["preference_type"]
    except (KeyError, TypeError):
        raise ConfigError(
            "preference_type is not specified properly in config.yaml, see example_config.yaml for an example"
        )
    if not isinstance(preference_type, str):
        raise ConfigError(
            "preference_type should be specified as a string in config.yaml, see example_config.yaml for an example"
        )
    if preference_type not in PREFERENCE_TYPES:
        raise ConfigError(
            f"preference_type should be one of {*PREFERENCE_TYPES,}, {preference_type} is not one of them"
        )

    logging.info("Parsing complete.")
    return preference_type


def _parse_log_file(config: dict) -> str:
    """Parses the log file from the config.yaml file.

    Args:
        config (dict): loaded config.yaml file

    Raises:
        ConfigError:

    Returns:
        str: parsed log file
    """
    print(
        "Parsing log file from config.yaml..."
    )  # not logging because logging is not initialized yet

    try:
        log_file = config["log_file"]
    except (KeyError, TypeError):
        raise ConfigError(
            "log_file is not specified properly in config.yaml, see example_config.yaml for an example"
        )
    if not isinstance(log_file, str):
        raise ConfigError(
            "log_file should be specified as a string in config.yaml, see example_config.yaml for an example"
        )

    print("Parsing complete.")
    return log_file


path_to_config_yaml = os.path.join(
    os.path.dirname(__file__), "../../config/config.yaml"
)
with open(path_to_config_yaml) as config_yaml:
    config = yaml.safe_load(config_yaml)

LOG_FILE = _parse_log_file(config)
init_logger(LOG_FILE)

PROPOSER_SIDE_NAME, RESPONDER_SIDE_NAME = _parse_proposer_and_responder(config)
logging.info(f"Proposer: {PROPOSER_SIDE_NAME}, Responder: {RESPONDER_SIDE_NAME}")

NUMBER_OF_PROPOSERS, NUMBER_OF_RESPONDERS = _parse_number_of_proposers_and_responders(
    config
)
logging.info(
    f"Number of proposers: {NUMBER_OF_PROPOSERS}, Number of responders: {NUMBER_OF_RESPONDERS}"
)

PREFERENCE_TYPE = _parse_preference_type(config)
logging.info(f"Preference type: {PREFERENCE_TYPE}")

parsed_config = [
    PROPOSER_SIDE_NAME,
    RESPONDER_SIDE_NAME,
    NUMBER_OF_PROPOSERS,
    NUMBER_OF_RESPONDERS,
    PREFERENCE_TYPE,
]
