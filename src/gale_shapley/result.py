"""Result types for the Gale-Shapley algorithm."""

from dataclasses import dataclass


@dataclass(frozen=True)
class MatchingResult:
    """Result of running the Gale-Shapley algorithm."""

    rounds: int
    matches: dict[str, str]
    unmatched: list[str]
    self_matches: list[str]
    all_matched: bool


@dataclass(frozen=True)
class StabilityResult:
    """Result of a stability check on a matching."""

    is_stable: bool
    is_individually_rational: bool
    blocking_pairs: list[tuple[str, str]]
