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
from config_parser import parsed_config
from simulator import Simulator

# %%
if __name__ == "__main__":
    sim = Simulator(*parsed_config)
    sim.number_of_simulations = 1000
    sim.simulate()
    # for i, algorithm in enumerate(sim.results):
    #     print(f"Simulation {i+1} took {algorithm.round} rounds")

# %%
