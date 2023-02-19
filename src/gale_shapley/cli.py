"""Command line application module for Gale-Shapley algorithm."""

import logging

from gale_shapley.config_parser import config_input
from gale_shapley.simulator import Simulator
from gale_shapley.utils import init_logger


def main() -> int:
    """Main function for Gale-Shapley algorithm. Logger is initialized here."""
    init_logger(config_input.log_file_name)
    logging.info("Parsing config.yaml is complete.")
    logging.info(
        f"Proposer side name: {config_input.proposer_side_name}, Responder side name: {config_input.responder_side_name}"
    )
    logging.info(
        f"Number of proposers: {config_input.number_of_proposers}, Number of responders: {config_input.number_of_responders}"
    )
    logging.info(f"Preference type: {config_input.preference_type}")

    sim = Simulator(config_input)
    sim.number_of_simulations = 1000  # TODO: Make this configurable
    sim.simulate()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
