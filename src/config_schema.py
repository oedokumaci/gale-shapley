"""This module contains the schema for the config.yaml file."""
import os.path

import yaml

from exceptions import ConfigError, TwoSidedMatchingError


def _parse_proposer_and_responder(config: dict) -> tuple[str, str]:
    """Parse the proposer and responder from the config.yaml file.

    Args:
        config (dict): loaded config.yaml file

    Raises:
        ConfigError
        TwoSidedMatchingError

    Returns:
        tuple[str, str]: proposer and responder
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
    if len(proposer_and_responder) != 2:
        raise TwoSidedMatchingError(proposer_and_responder)
    proposer, responder = proposer_and_responder
    if not isinstance(proposer, str):
        raise ConfigError(f"Proposer should be a string, {proposer} is not a string")
    if not isinstance(responder, str):
        raise ConfigError(f"Responder should be a string, {responder} is not a string")
    print("Parsing complete.")
    return proposer, responder


if __name__ == "__main__":
    path_to_config_yaml = os.path.join(
        os.path.dirname(__file__), "../config/config.yaml"
    )
    with open(path_to_config_yaml) as config_yaml:
        config = yaml.safe_load(config_yaml)
    PROPOSER, RESPONDER = _parse_proposer_and_responder(config)
    print(f"Proposer: {PROPOSER}, Responder: {RESPONDER}")
