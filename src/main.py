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
from algorithm import Algorithm
from create_objects import proposers, responders

# %%
if __name__ == "__main__":
    gs_algorithm = Algorithm(proposers, responders)
    gs_algorithm.run()

# %%
