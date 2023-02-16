"""Main module for Gale-Shapley algorithm."""

from gale_shapley.config_parser import parsed_config
from gale_shapley.simulator import Simulator


def main() -> int:
    """Main function for Gale-Shapley algorithm."""
    sim = Simulator(*parsed_config)
    sim.number_of_simulations = 1000
    sim.simulate()
    # for i, algorithm in enumerate(sim.results):
    #     print(f"Simulation {i+1} took {algorithm.round} rounds")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
