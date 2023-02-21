"""Command line application module for Gale-Shapley algorithm."""

import typer

from gale_shapley.config_parser import config_input
from gale_shapley.simulator import Simulator
from gale_shapley.utils import LOG_PATH, init_logger, log_config_info

number_of_simulations_typer_argument = typer.Argument(
    100, min=1, help="Desired number of simulations"
)
print_all_preferences_typer_option = typer.Option(True, help="Print preferences of all")
compact_typer_option = typer.Option(
    True, help="Prints all preferences in one table compactly"
)
report_matches_typer_option = typer.Option(
    True, help="Reports the final matching of each simulation"
)


def main(
    number_of_simulations: int = number_of_simulations_typer_argument,
    print_all_preferences: bool = print_all_preferences_typer_option,
    compact: bool = compact_typer_option,
    report_matches: bool = report_matches_typer_option,
) -> None:
    """Simulates the Gale-Shapley Algorithm desired times and logs the results."""
    init_logger(config_input.log_file_name)  # Logger is initialized here.
    log_config_info(config_input)

    sim = Simulator(config_input)
    sim.number_of_simulations = number_of_simulations
    sim.simulate(
        print_all_preferences=print_all_preferences,
        compact=compact,
        report_matches=report_matches,
    )

    print("")
    print(f"Logs are saved to {(LOG_PATH / config_input.log_file_name).resolve()}")
    raise typer.Exit()
