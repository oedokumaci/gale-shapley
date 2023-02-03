# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: -all
#     custom_cell_magics: kql
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.11.2
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %%
import random

from algorithm import Algorithm
from config_parser import NUMBER_OF_PROPOSERS, NUMBER_OF_RESPONDERS, PROPOSER, RESPONDER
from proposer_responder import Proposer, Responder


# %%
def create_objects(
    proposer_name: str,
    responder_name: str,
    number_of_proposers: int,
    number_of_responders: int,
) -> tuple[list[Proposer], list[Responder]]:
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


# %%
if __name__ == "__main__":
    proposers, responders = create_objects(
        PROPOSER, RESPONDER, NUMBER_OF_PROPOSERS, NUMBER_OF_RESPONDERS
    )
    gs_algorithm = Algorithm(proposers, responders)
    gs_algorithm.run()
