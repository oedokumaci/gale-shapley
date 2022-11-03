import os.path
from typing import (  # need for Python<3.9, # List imported from exceptions.py below
    Dict,
    Tuple,
)

import yaml

from exceptions import ConfigError, List, SideNameError, TwoSidedMatchingError


def _parse_proposer_and_responder(
    side: str, config: Dict, side_names: List
) -> Tuple[str, str]:
    if side == "PROPOSER":
        proposer = config[side]
        if proposer not in side_names:
            raise SideNameError(side, side_names)
        responder = [side for side in side_names if side != proposer][0]
    elif side == "RESPONDER":
        responder = config[side]
        if responder not in side_names:
            raise SideNameError(side, side_names)
        proposer = [side for side in side_names if side != responder][0]
    if not isinstance(proposer, str):
        raise ConfigError("PROPOSER should be a string")
    if not isinstance(responder, str):
        raise ConfigError("RESPONDER should be a string")
    print(f"Proposer: {proposer}, Responder: {responder}")
    return proposer, responder


path_to_config_yaml = os.path.join(os.path.dirname(__file__), "../config/config.yaml")
with open(path_to_config_yaml) as config_yaml:
    config = yaml.safe_load(config_yaml)

SIDE_NAMES = config["SIDE_NAMES"]
if not isinstance(SIDE_NAMES, list):
    raise ConfigError("SIDE_NAMES should be a list")

if len(SIDE_NAMES) != 2:
    raise TwoSidedMatchingError(SIDE_NAMES)

try:
    PROPOSER, RESPONDER = _parse_proposer_and_responder("PROPOSER", config, SIDE_NAMES)
except KeyError:
    try:
        PROPOSER, RESPONDER = _parse_proposer_and_responder(
            "RESPONDER", config, SIDE_NAMES
        )
    except KeyError:
        raise ConfigError("Either PROPOSER or RESPONDER has to be in config.yaml")
