"""Interactive prompt functions for the CLI."""

from rich.console import Console
from rich.prompt import IntPrompt, Prompt

console = Console()


def prompt_side_names() -> tuple[str, str]:
    """Prompt for proposer and responder side names.

    Returns:
        Tuple of (proposer_side_name, responder_side_name).
    """
    proposer_name = Prompt.ask("Enter proposer side name", default="Proposers")
    responder_name = Prompt.ask("Enter responder side name", default="Responders")

    if proposer_name.casefold() == responder_name.casefold():
        console.print("[red]Side names must be different.[/red]")
        return prompt_side_names()

    return proposer_name, responder_name


def prompt_names(side_name: str) -> list[str]:
    """Prompt for person names on a given side.

    Args:
        side_name: The side label (e.g. "Men").

    Returns:
        List of trimmed, non-empty names.
    """
    raw = Prompt.ask(f"Enter names for {side_name} (comma-separated)")
    names = [n.strip() for n in raw.split(",") if n.strip()]

    if not names:
        console.print("[red]Please enter at least one name.[/red]")
        return prompt_names(side_name)

    if len(names) != len(set(names)):
        console.print("[red]Names must be unique.[/red]")
        return prompt_names(side_name)

    return names


def prompt_preferences(side_name: str, names: list[str], other_names: list[str]) -> dict[str, list[str]]:
    """Prompt for preference rankings for each person on a side.

    Displays a numbered list of the other side's names and asks the user
    to enter comma-separated indices to define the ranking.

    Args:
        side_name: The side label (e.g. "Men").
        names: Names on this side.
        other_names: Names on the other side.

    Returns:
        Dict mapping each name to their ordered preference list.
    """
    console.print(f"\nRanking preferences for [bold]{side_name}[/bold]...")
    preferences: dict[str, list[str]] = {}

    for name in names:
        console.print(f"\n  Available for [bold]{name}[/bold]:")
        for i, other in enumerate(other_names, 1):
            console.print(f"  {i}. {other}")

        ranking = _prompt_ranking(name, other_names)
        preferences[name] = ranking
        console.print(f"  → {name}: {' > '.join(ranking)}")

    return preferences


def _prompt_ranking(name: str, other_names: list[str]) -> list[str]:
    """Prompt a single person for their preference ranking.

    Args:
        name: The person being prompted.
        other_names: Available choices.

    Returns:
        Ordered list of preferred names.
    """
    example = ",".join(str(i) for i in range(1, len(other_names) + 1))
    raw = Prompt.ask(f"  Enter ranking for {name} (e.g. {example})")
    parts = [p.strip() for p in raw.split(",") if p.strip()]

    try:
        indices = [int(p) for p in parts]
    except ValueError:
        console.print("  [red]Please enter comma-separated numbers.[/red]")
        return _prompt_ranking(name, other_names)

    if not indices:
        console.print("  [red]Please enter at least one number.[/red]")
        return _prompt_ranking(name, other_names)

    if any(i < 1 or i > len(other_names) for i in indices):
        console.print(f"  [red]Numbers must be between 1 and {len(other_names)}.[/red]")
        return _prompt_ranking(name, other_names)

    if len(indices) != len(set(indices)):
        console.print("  [red]No duplicates allowed.[/red]")
        return _prompt_ranking(name, other_names)

    return [other_names[i - 1] for i in indices]


def prompt_random_config() -> tuple[str, str, int, int]:
    """Prompt for random mode configuration.

    Returns:
        Tuple of (proposer_side_name, responder_side_name, num_proposers, num_responders).
    """
    proposer_name, responder_name = prompt_side_names()
    num_proposers = IntPrompt.ask(f"Number of {proposer_name}", default=3)
    num_responders = IntPrompt.ask(f"Number of {responder_name}", default=3)

    if num_proposers < 1 or num_responders < 1:
        console.print("[red]Counts must be at least 1.[/red]")
        return prompt_random_config()

    return proposer_name, responder_name, num_proposers, num_responders
