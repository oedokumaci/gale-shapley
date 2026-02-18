"""Command line application module for Gale-Shapley algorithm."""

import random
from typing import TYPE_CHECKING

import typer

from gale_shapley_algorithm._cli import console
from gale_shapley_algorithm._cli.display import display_preferences, display_results
from gale_shapley_algorithm._cli.prompts import (
    prompt_names,
    prompt_preferences,
    prompt_random_config,
    prompt_side_names,
)
from gale_shapley_algorithm.matching import _build_algorithm
from gale_shapley_algorithm.stability import check_stability

if TYPE_CHECKING:
    from gale_shapley_algorithm.result import MatchingResult, StabilityResult

app = typer.Typer(help="Gale-Shapley Algorithm — interactive matching.")


def _run_matching(
    proposer_prefs: dict[str, list[str]],
    responder_prefs: dict[str, list[str]],
) -> tuple["MatchingResult", "StabilityResult"]:
    """Build an Algorithm from preference dicts, execute, and check stability.

    Incomplete preference lists are padded: self is appended (for self-matching
    as a fallback), followed by any members of the other side not already listed.

    Args:
        proposer_prefs: Mapping of proposer names to ordered list of responder names.
            Need not be complete — missing responders are appended in arbitrary order.
        responder_prefs: Mapping of responder names to ordered list of proposer names.
            Need not be complete — missing proposers are appended in arbitrary order.

    Returns:
        Tuple of (MatchingResult, StabilityResult).
    """
    algorithm = _build_algorithm(proposer_prefs, responder_prefs)
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

    Generated names use the first character of each side name as a prefix
    (e.g. "m_1", "w_1"). If both sides share the same first character,
    the full lowercased side name is used instead to avoid collisions.

    Args:
        proposer_side: Proposer side name (used to derive generated names).
        responder_side: Responder side name (used to derive generated names).
        num_proposers: Number of proposers to generate.
        num_responders: Number of responders to generate.

    Returns:
        Tuple of (proposer_preferences, responder_preferences) where each
        is a dict mapping generated names to a randomly shuffled list of
        the other side's names.
    """
    p_short = proposer_side[0].lower()
    r_short = responder_side[0].lower()
    if p_short == r_short:
        p_short = proposer_side.lower()
        r_short = responder_side.lower()

    p_names = [f"{p_short}_{i}" for i in range(1, num_proposers + 1)]
    r_names = [f"{r_short}_{i}" for i in range(1, num_responders + 1)]

    proposer_prefs = {name: random.sample(r_names, len(r_names)) for name in p_names}
    responder_prefs = {name: random.sample(p_names, len(p_names)) for name in r_names}

    return proposer_prefs, responder_prefs


@app.command()
def main(
    random_mode: bool = typer.Option(False, "--random", help="Generate random preferences"),
    swap_sides: bool = typer.Option(False, "--swap-sides", help="Swap proposers and responders"),
) -> None:
    """Run the Gale-Shapley algorithm interactively.

    Supports manual preference entry or random generation (--random).
    Use --swap-sides to reverse proposer/responder roles before matching.
    """
    try:
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
    except KeyboardInterrupt:
        console.print("\n[yellow]Interrupted.[/yellow]")
        raise typer.Exit(code=130) from None
    except EOFError:
        console.print("\n[yellow]Input stream closed.[/yellow]")
        raise typer.Exit(code=1) from None
