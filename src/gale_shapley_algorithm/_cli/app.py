"""Command line application module for Gale-Shapley algorithm."""

import random
from typing import TYPE_CHECKING

import typer
from rich.console import Console

from gale_shapley_algorithm._cli.display import display_preferences, display_results
from gale_shapley_algorithm._cli.prompts import (
    prompt_names,
    prompt_preferences,
    prompt_random_config,
    prompt_side_names,
)
from gale_shapley_algorithm.algorithm import Algorithm
from gale_shapley_algorithm.person import Proposer, Responder
from gale_shapley_algorithm.stability import check_stability

if TYPE_CHECKING:
    from gale_shapley_algorithm.result import MatchingResult, StabilityResult

console = Console()
app = typer.Typer(help="Gale-Shapley Algorithm — interactive matching.")


def _run_matching(
    proposer_prefs: dict[str, list[str]],
    responder_prefs: dict[str, list[str]],
) -> tuple["MatchingResult", "StabilityResult"]:
    """Build an Algorithm from preference dicts, execute, and check stability.

    Args:
        proposer_prefs: Mapping of proposer names to ordered list of responder names.
        responder_prefs: Mapping of responder names to ordered list of proposer names.

    Returns:
        Tuple of (MatchingResult, StabilityResult).
    """
    proposers = {name: Proposer(name, "proposer") for name in proposer_prefs}
    responders = {name: Responder(name, "responder") for name in responder_prefs}

    for name, pref_names in proposer_prefs.items():
        p = proposers[name]
        prefs: list[Proposer | Responder] = [responders[r] for r in pref_names if r in responders]
        if p not in prefs:
            prefs.append(p)
        for r in responders.values():
            if r not in prefs:
                prefs.append(r)
        p.preferences = tuple(prefs)

    for name, pref_names in responder_prefs.items():
        r = responders[name]
        prefs_r: list[Proposer | Responder] = [proposers[p] for p in pref_names if p in proposers]
        if r not in prefs_r:
            prefs_r.append(r)
        for p in proposers.values():
            if p not in prefs_r:
                prefs_r.append(p)
        r.preferences = tuple(prefs_r)

    algorithm = Algorithm(list(proposers.values()), list(responders.values()))
    result = algorithm.execute()
    stability = check_stability(algorithm)
    return result, stability


def _generate_random_preferences(
    proposer_side: str,
    responder_side: str,
    num_proposers: int,
    num_responders: int,
) -> tuple[dict[str, list[str]], dict[str, list[str]]]:
    """Generate random preference dicts for both sides.

    Args:
        proposer_side: Proposer side name.
        responder_side: Responder side name.
        num_proposers: Number of proposers.
        num_responders: Number of responders.

    Returns:
        Tuple of (proposer_preferences, responder_preferences).
    """
    p_short = proposer_side[0].lower()
    r_short = responder_side[0].lower()
    if p_short == r_short:
        p_short = proposer_side.lower()
        r_short = responder_side.lower()

    p_names = [f"{p_short}_{i}" for i in range(1, num_proposers + 1)]
    r_names = [f"{r_short}_{i}" for i in range(1, num_responders + 1)]

    proposer_prefs: dict[str, list[str]] = {}
    for name in p_names:
        shuffled = r_names.copy()
        random.shuffle(shuffled)
        proposer_prefs[name] = shuffled

    responder_prefs: dict[str, list[str]] = {}
    for name in r_names:
        shuffled = p_names.copy()
        random.shuffle(shuffled)
        responder_prefs[name] = shuffled

    return proposer_prefs, responder_prefs


@app.command()
def main(
    random_mode: bool = typer.Option(False, "--random", help="Generate random preferences"),
    swap_sides: bool = typer.Option(False, "--swap-sides", help="Swap proposers and responders"),
) -> None:
    """Run the Gale-Shapley algorithm interactively."""
    console.print("\n[bold]Gale-Shapley Algorithm[/bold]\n")

    if random_mode:
        proposer_side, responder_side, num_p, num_r = prompt_random_config()
        proposer_prefs, responder_prefs = _generate_random_preferences(proposer_side, responder_side, num_p, num_r)
    else:
        proposer_side, responder_side = prompt_side_names()
        p_names = prompt_names(proposer_side)
        r_names = prompt_names(responder_side)
        proposer_prefs = prompt_preferences(proposer_side, p_names, r_names)
        responder_prefs = prompt_preferences(responder_side, r_names, p_names)

    if swap_sides:
        proposer_side, responder_side = responder_side, proposer_side
        proposer_prefs, responder_prefs = responder_prefs, proposer_prefs

    display_preferences(proposer_side, responder_side, proposer_prefs, responder_prefs)

    result, stability = _run_matching(proposer_prefs, responder_prefs)

    display_results(proposer_side, responder_side, result, stability)
