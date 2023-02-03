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

from config_parser import (
    NUMBER_OF_PROPOSERS,
    NUMBER_OF_RESPONDERS,
    PROPOSER_SIDE_NAME,
    RESPONDER_SIDE_NAME,
)

# %%
from simulator import Simulator

# %%
if __name__ == "__main__":
    sim = Simulator(
        PROPOSER_SIDE_NAME,
        RESPONDER_SIDE_NAME,
        NUMBER_OF_PROPOSERS,
        NUMBER_OF_RESPONDERS,
    )
    sim.number_of_simulations = 10
    sim.run()
    for i, algorithm in enumerate(sim.results):
        print(f"Simulation {i+1} took {algorithm.round} rounds")

# %%
