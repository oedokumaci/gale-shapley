"""Tests for the create_matching convenience function."""

from gale_shapley_algorithm.matching import create_matching
from gale_shapley_algorithm.result import MatchingResult


class TestCreateMatching:
    """Tests for create_matching."""

    def test_basic_matching(self) -> None:
        result = create_matching(
            proposer_preferences={"alice": ["bob", "charlie"], "dave": ["charlie", "bob"]},
            responder_preferences={"bob": ["alice", "dave"], "charlie": ["dave", "alice"]},
        )
        assert isinstance(result, MatchingResult)
        assert result.all_matched
        assert len(result.matches) == 2

    def test_deterministic_result(self) -> None:
        """GS always produces proposer-optimal stable matching."""
        result = create_matching(
            proposer_preferences={"m1": ["w1", "w2"], "m2": ["w1", "w2"]},
            responder_preferences={"w1": ["m1", "m2"], "w2": ["m1", "m2"]},
        )
        # m1 gets w1 (proposer-optimal)
        assert result.matches["m1"] == "w1"
        assert result.matches["m2"] == "w2"

    def test_unequal_sides(self) -> None:
        """More proposers than responders leads to self-matches."""
        result = create_matching(
            proposer_preferences={"m1": ["w1"], "m2": ["w1"], "m3": ["w1"]},
            responder_preferences={"w1": ["m1", "m2", "m3"]},
        )
        assert isinstance(result, MatchingResult)
        # Only one can match w1
        assert len(result.matches) == 1
        assert len(result.self_matches) > 0

    def test_empty_preferences(self) -> None:
        """Empty preference lists result in self-matches."""
        result = create_matching(
            proposer_preferences={"m1": []},
            responder_preferences={"w1": []},
        )
        assert "m1" in result.self_matches
        assert "w1" in result.self_matches
        assert not result.all_matched
