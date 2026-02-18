"""gale-shapley: A Python implementation of the Gale-Shapley algorithm."""

from gale_shapley.algorithm import Algorithm
from gale_shapley.matching import create_matching
from gale_shapley.person import Person, Proposer, Responder
from gale_shapley.result import MatchingResult, StabilityResult
from gale_shapley.stability import check_stability, find_blocking_pairs, is_individually_rational

__version__ = "1.1.1"
__all__ = [
    "Algorithm",
    "MatchingResult",
    "Person",
    "Proposer",
    "Responder",
    "StabilityResult",
    "check_stability",
    "create_matching",
    "find_blocking_pairs",
    "is_individually_rational",
]
