"""This module creates the objects for the algorithm."""
import random

from config_parser import (
    NUMBER_OF_PROPOSERS,
    NUMBER_OF_RESPONDERS,
    PROPOSER_SIDE_NAME,
    RESPONDER_SIDE_NAME,
)
from proposer_responder import Proposer, Responder


def create_objects(
    proposer_name: str,
    responder_name: str,
    number_of_proposers: int,
    number_of_responders: int,
) -> tuple[list[Proposer], list[Responder]]:
    """Creates the objects for the algorithm.

    Args:
        proposer_name (str): parsed from config.yaml
        responder_name (str): parsed from config.yaml
        number_of_proposers (int): parsed from config.yaml
        number_of_responders (int): parsed from config.yaml

    Returns:
        tuple[list[Proposer], list[Responder]]: list of proposers and list of responders
    """
    if proposer_name[0] != responder_name[0]:
        proposers = [
            Proposer(f"{proposer_name[0]}_{i+1}", proposer_name)
            for i in range(number_of_proposers)
        ]
        responders = [
            Responder(f"{responder_name[0]}_{i+1}", responder_name)
            for i in range(number_of_responders)
        ]
    else:
        proposers = [
            Proposer(f"{proposer_name}_{i+1}", proposer_name)
            for i in range(number_of_proposers)
        ]
        responders = [
            Responder(f"{responder_name}_{i+1}", responder_name)
            for i in range(number_of_responders)
        ]

    for proposer in proposers:
        select_from = [proposer] + responders
        random.shuffle(select_from)
        proposer.preferences = tuple(select_from)
    for responder in responders:
        select_from = [responder] + proposers
        random.shuffle(select_from)
        responder.preferences = tuple(select_from)

    return proposers, responders


proposers, responders = create_objects(
    PROPOSER_SIDE_NAME, RESPONDER_SIDE_NAME, NUMBER_OF_PROPOSERS, NUMBER_OF_RESPONDERS
)
