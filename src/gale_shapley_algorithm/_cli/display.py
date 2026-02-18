"""Rich output formatting for the CLI."""

from typing import TYPE_CHECKING

from rich.console import Console
from rich.table import Table

if TYPE_CHECKING:
    from gale_shapley_algorithm.result import MatchingResult, StabilityResult

console = Console()


def display_preferences(
    proposer_side: str,
    responder_side: str,
    proposer_prefs: dict[str, list[str]],
    responder_prefs: dict[str, list[str]],
) -> None:
    """Display preference tables for both sides.

    Args:
        proposer_side: Proposer side name.
        responder_side: Responder side name.
        proposer_prefs: Proposer preference dicts.
        responder_prefs: Responder preference dicts.
    """
    _display_side_preferences(proposer_side, proposer_prefs)
    _display_side_preferences(responder_side, responder_prefs)


def _display_side_preferences(side_name: str, preferences: dict[str, list[str]]) -> None:
    """Display a preference table for one side.

    Args:
        side_name: The side label.
        preferences: Dict mapping names to ordered preference lists.
    """
    table = Table(title=f"{side_name} Preferences")
    table.add_column("Person", style="bold")
    table.add_column("Preferences (most → least preferred)")

    for name, prefs in preferences.items():
        table.add_row(name, " > ".join(prefs) if prefs else "(none)")

    console.print(table)


def display_results(
    proposer_side: str,
    responder_side: str,
    result: "MatchingResult",
    stability: "StabilityResult",
) -> None:
    """Display matching results and stability info.

    Args:
        proposer_side: Proposer side name.
        responder_side: Responder side name.
        result: The matching result.
        stability: The stability check result.
    """
    table = Table(title="Matching Result")
    table.add_column(proposer_side, style="bold cyan")
    table.add_column(responder_side, style="bold green")

    for proposer, responder in result.matches.items():
        table.add_row(proposer, responder)

    if result.self_matches:
        for name in result.self_matches:
            table.add_row(name, "(self)")

    if result.unmatched:
        for name in result.unmatched:
            table.add_row(name, "(unmatched)")

    console.print()
    console.print(table)
    console.print(
        f"Completed in {result.rounds} round{'s' if result.rounds != 1 else ''}. Stable: {'Yes' if stability.is_stable else 'No'}"
    )

    if stability.blocking_pairs:
        console.print(f"[yellow]Blocking pairs: {stability.blocking_pairs}[/yellow]")
