"""Command line application module for Gale-Shapley algorithm."""

from typing import Final, NoReturn

import typer
from rich import print as rprint

from gale_shapley_algorithm._cli.config import load_config, side_swap
from gale_shapley_algorithm._cli.logging import LOG_PATH, init_logger, log_config_info
from gale_shapley_algorithm._cli.simulator import Simulator

number_of_simulations_argument: Final = typer.Argument(1, min=1, help="Desired number of simulations")
print_all_preferences_option: Final = typer.Option(True, help="Print preferences of all")
compact_option: Final = typer.Option(True, help="Prints all preferences in one table compactly")
report_matches_option: Final = typer.Option(True, help="Reports the final matching of each simulation")
swap_sides_option: Final = typer.Option(False, help="Swaps proposers and responders")


def main(
    number_of_simulations: int = number_of_simulations_argument,
    print_all_preferences: bool = print_all_preferences_option,
    compact: bool = compact_option,
    report_matches: bool = report_matches_option,
    swap_sides: bool = swap_sides_option,
) -> NoReturn:
    """Simulates the Gale-Shapley Algorithm desired times and logs the results."""
    config_input = load_config()

    # Check if log file exists, if so ask to overwrite
    log_file = LOG_PATH / config_input.log_file_name
    if log_file.exists():
        user_input = input(f"log_file_name {config_input.log_file_name!r} already exists, overwrite? y/n (n): ") or "n"
        match user_input:
            case "y":
                pass
            case _:
                raise SystemExit("exiting not to overwrite, please change 'log_file_name' in 'config.yaml'")
        rprint("")

    # Initialize logger
    init_logger(config_input.log_file_name)

    # Log config info
    if swap_sides:
        side_swap(config_input)
    log_config_info(config_input)

    # Simulate
    sim = Simulator(config_input)
    sim.number_of_simulations = number_of_simulations
    sim.simulate(
        print_all_preferences=print_all_preferences,
        compact=compact,
        report_matches=report_matches,
    )

    # Print log file path
    rprint("")
    rprint(f"logs are saved to {log_file.resolve()}")

    raise typer.Exit
