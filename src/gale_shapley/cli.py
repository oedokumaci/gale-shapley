"""Command line application module for Gale-Shapley algorithm."""

from gale_shapley.config_parser import config_input
from gale_shapley.simulator import Simulator


def main() -> int:
    """Main function for Gale-Shapley algorithm."""
    sim = Simulator(config_input)
    sim.number_of_simulations = 1000  # TODO: Make this configurable
    sim.simulate()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
