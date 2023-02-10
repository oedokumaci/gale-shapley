"""This module contains the schema for the config.yaml file and parses it when imported."""

import os.path

import yaml

from exceptions import ConfigError, TwoSidedMatchingError


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
    print("Parsing proposer and responder from config.yaml...")

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

    print("Parsing complete.")
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
    print("Parsing number of proposers and responders from config.yaml...")

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

    print("Parsing complete.")
    return number_of_proposers, number_of_responders


path_to_config_yaml = os.path.join(os.path.dirname(__file__), "../config/config.yaml")
with open(path_to_config_yaml) as config_yaml:
    config = yaml.safe_load(config_yaml)

PROPOSER_SIDE_NAME, RESPONDER_SIDE_NAME = _parse_proposer_and_responder(config)
print(f"Proposer: {PROPOSER_SIDE_NAME}, Responder: {RESPONDER_SIDE_NAME}")

NUMBER_OF_PROPOSERS, NUMBER_OF_RESPONDERS = _parse_number_of_proposers_and_responders(
    config
)
print(
    f"Number of proposers: {NUMBER_OF_PROPOSERS}, Number of responders: {NUMBER_OF_RESPONDERS}"
)

parsed_config = [
    PROPOSER_SIDE_NAME,
    RESPONDER_SIDE_NAME,
    NUMBER_OF_PROPOSERS,
    NUMBER_OF_RESPONDERS,
]
