"""Convenience function for creating matchings."""

from gale_shapley.algorithm import Algorithm
from gale_shapley.person import Proposer, Responder
from gale_shapley.result import MatchingResult


def create_matching(
    proposer_preferences: dict[str, list[str]],
    responder_preferences: dict[str, list[str]],
) -> MatchingResult:
    """Create a matching from preference dictionaries.

    This is the simplest way to use the library. Provide preference rankings
    for each side and get back a MatchingResult.

    Persons not listed in a preference list are considered unacceptable.
    Each person is automatically added to their own preference list at the end
    (making everyone they listed acceptable).

    Args:
        proposer_preferences: Mapping of proposer names to ordered list of responder names.
        responder_preferences: Mapping of responder names to ordered list of proposer names.

    Returns:
        MatchingResult with the matching outcome.

    Example:
        >>> result = create_matching(
        ...     proposer_preferences={"alice": ["bob", "charlie"], "dave": ["charlie", "bob"]},
        ...     responder_preferences={"bob": ["alice", "dave"], "charlie": ["dave", "alice"]},
        ... )
        >>> result.matches
        {'alice': 'bob', 'dave': 'charlie'}
    """
    proposers = {name: Proposer(name, "proposer") for name in proposer_preferences}
    responders = {name: Responder(name, "responder") for name in responder_preferences}

    for name, pref_names in proposer_preferences.items():
        p = proposers[name]
        prefs: list[Proposer | Responder] = [responders[r] for r in pref_names if r in responders]
        if p not in prefs:
            prefs.append(p)
        # Add unlisted responders after self (unacceptable)
        for r in responders.values():
            if r not in prefs:
                prefs.append(r)
        p.preferences = tuple(prefs)

    for name, pref_names in responder_preferences.items():
        r = responders[name]
        prefs_r: list[Proposer | Responder] = [proposers[p] for p in pref_names if p in proposers]
        if r not in prefs_r:
            prefs_r.append(r)
        for p in proposers.values():
            if p not in prefs_r:
                prefs_r.append(p)
        r.preferences = tuple(prefs_r)

    algorithm = Algorithm(list(proposers.values()), list(responders.values()))
    return algorithm.execute()
