"""Tests for the CLI module."""

from unittest.mock import patch

import pytest
from typer.testing import CliRunner

from gale_shapley_algorithm._cli.app import app
from gale_shapley_algorithm._cli.prompts import (
    _prompt_ranking,
    prompt_names,
    prompt_preferences,
    prompt_random_config,
    prompt_side_names,
)

runner = CliRunner()


# --- Integration tests (full CLI) ---


def test_cli_interactive_mode() -> None:
    """Test CLI in interactive mode with monkeypatched prompts."""
    with (
        patch(
            "gale_shapley_algorithm._cli.app.prompt_side_names",
            return_value=("Men", "Women"),
        ),
        patch(
            "gale_shapley_algorithm._cli.app.prompt_names",
            side_effect=[["Will", "Hampton"], ["April", "Summer"]],
        ),
        patch(
            "gale_shapley_algorithm._cli.app.prompt_preferences",
            side_effect=[
                {"Will": ["April", "Summer"], "Hampton": ["Summer", "April"]},
                {"April": ["Will", "Hampton"], "Summer": ["Hampton", "Will"]},
            ],
        ),
    ):
        result = runner.invoke(app, [])

    assert result.exit_code == 0
    assert "Matching Result" in result.output


def test_cli_random_mode() -> None:
    """Test CLI in random mode."""
    with patch(
        "gale_shapley_algorithm._cli.app.prompt_random_config",
        return_value=("Men", "Women", 3, 3),
    ):
        result = runner.invoke(app, ["--random"])

    assert result.exit_code == 0
    assert "Matching Result" in result.output


def test_cli_swap_sides() -> None:
    """Test CLI with --swap-sides runs algorithm twice and shows both results."""
    with (
        patch(
            "gale_shapley_algorithm._cli.app.prompt_side_names",
            return_value=("Men", "Women"),
        ),
        patch(
            "gale_shapley_algorithm._cli.app.prompt_names",
            side_effect=[["Will", "Hampton"], ["April", "Summer"]],
        ),
        patch(
            "gale_shapley_algorithm._cli.app.prompt_preferences",
            side_effect=[
                {"Will": ["April", "Summer"], "Hampton": ["Summer", "April"]},
                {"April": ["Will", "Hampton"], "Summer": ["Hampton", "Will"]},
            ],
        ),
    ):
        result = runner.invoke(app, ["--swap-sides"])

    assert result.exit_code == 0
    assert "Men proposing" in result.output
    assert "Women proposing" in result.output
    assert result.output.count("Matching Result") == 2


def test_cli_random_mode_with_swap() -> None:
    """Test CLI in random mode with --swap-sides runs twice."""
    with patch(
        "gale_shapley_algorithm._cli.app.prompt_random_config",
        return_value=("Men", "Women", 2, 2),
    ):
        result = runner.invoke(app, ["--random", "--swap-sides"])

    assert result.exit_code == 0
    assert "Men proposing" in result.output
    assert "Women proposing" in result.output
    assert result.output.count("Matching Result") == 2


def test_cli_keyboard_interrupt() -> None:
    """Test CLI handles KeyboardInterrupt gracefully."""
    with patch(
        "gale_shapley_algorithm._cli.app.prompt_random_config",
        side_effect=KeyboardInterrupt,
    ):
        result = runner.invoke(app, ["--random"])

    assert result.exit_code == 130
    assert "Interrupted" in result.output


def test_cli_eof_error() -> None:
    """Test CLI handles EOFError gracefully."""
    with patch(
        "gale_shapley_algorithm._cli.app.prompt_random_config",
        side_effect=EOFError,
    ):
        result = runner.invoke(app, ["--random"])

    assert result.exit_code == 1
    assert "Input stream closed" in result.output


def test_cli_stability_reported() -> None:
    """Test that stability is reported in output."""
    with patch(
        "gale_shapley_algorithm._cli.app.prompt_random_config",
        return_value=("Men", "Women", 2, 2),
    ):
        result = runner.invoke(app, ["--random"])

    assert result.exit_code == 0
    assert "Stable:" in result.output


# --- Unit tests for prompts.py ---


class TestPromptSideNames:
    """Tests for prompt_side_names."""

    def test_valid_names(self) -> None:
        with patch("gale_shapley_algorithm._cli.prompts.Prompt.ask", side_effect=["Men", "Women"]):
            result = prompt_side_names()
        assert result == ("Men", "Women")

    def test_same_names_retries(self) -> None:
        """When same names given, retries."""
        with patch(
            "gale_shapley_algorithm._cli.prompts.Prompt.ask",
            side_effect=["Men", "Men", "Men", "Women"],
        ):
            result = prompt_side_names()
        assert result == ("Men", "Women")


class TestPromptNames:
    """Tests for prompt_names."""

    def test_valid_names(self) -> None:
        with patch("gale_shapley_algorithm._cli.prompts.Prompt.ask", return_value="Alice, Bob"):
            result = prompt_names("Team")
        assert result == ["Alice", "Bob"]

    def test_empty_retries(self) -> None:
        with patch(
            "gale_shapley_algorithm._cli.prompts.Prompt.ask",
            side_effect=["", "Alice"],
        ):
            result = prompt_names("Team")
        assert result == ["Alice"]

    def test_duplicate_names_retries(self) -> None:
        with patch(
            "gale_shapley_algorithm._cli.prompts.Prompt.ask",
            side_effect=["Alice, Alice", "Alice, Bob"],
        ):
            result = prompt_names("Team")
        assert result == ["Alice", "Bob"]


class TestPromptRanking:
    """Tests for _prompt_ranking."""

    def test_valid_ranking(self) -> None:
        with patch("gale_shapley_algorithm._cli.prompts.Prompt.ask", return_value="2,1"):
            result = _prompt_ranking("Alice", ["Bob", "Charlie"])
        assert result == ["Charlie", "Bob"]

    def test_non_numeric_retries(self) -> None:
        with patch(
            "gale_shapley_algorithm._cli.prompts.Prompt.ask",
            side_effect=["a,b", "1,2"],
        ):
            result = _prompt_ranking("Alice", ["Bob", "Charlie"])
        assert result == ["Bob", "Charlie"]

    def test_empty_retries(self) -> None:
        with patch(
            "gale_shapley_algorithm._cli.prompts.Prompt.ask",
            side_effect=["", "1"],
        ):
            result = _prompt_ranking("Alice", ["Bob"])
        assert result == ["Bob"]

    def test_out_of_range_retries(self) -> None:
        with patch(
            "gale_shapley_algorithm._cli.prompts.Prompt.ask",
            side_effect=["0,3", "1,2"],
        ):
            result = _prompt_ranking("Alice", ["Bob", "Charlie"])
        assert result == ["Bob", "Charlie"]

    def test_duplicates_retries(self) -> None:
        with patch(
            "gale_shapley_algorithm._cli.prompts.Prompt.ask",
            side_effect=["1,1", "1,2"],
        ):
            result = _prompt_ranking("Alice", ["Bob", "Charlie"])
        assert result == ["Bob", "Charlie"]

    def test_partial_ranking(self) -> None:
        """User can rank fewer than all options."""
        with patch("gale_shapley_algorithm._cli.prompts.Prompt.ask", return_value="2"):
            result = _prompt_ranking("Alice", ["Bob", "Charlie"])
        assert result == ["Charlie"]


class TestPromptPreferences:
    """Tests for prompt_preferences."""

    def test_basic_flow(self) -> None:
        with patch(
            "gale_shapley_algorithm._cli.prompts.Prompt.ask",
            side_effect=["1,2", "2,1"],
        ):
            result = prompt_preferences("Men", ["Will", "Hampton"], ["April", "Summer"])
        assert result == {
            "Will": ["April", "Summer"],
            "Hampton": ["Summer", "April"],
        }


class TestPromptRandomConfig:
    """Tests for prompt_random_config."""

    def test_valid_config(self) -> None:
        with (
            patch(
                "gale_shapley_algorithm._cli.prompts.Prompt.ask",
                side_effect=["Men", "Women"],
            ),
            patch(
                "gale_shapley_algorithm._cli.prompts.IntPrompt.ask",
                side_effect=[3, 4],
            ),
        ):
            result = prompt_random_config()
        assert result == ("Men", "Women", 3, 4)

    def test_zero_count_retries(self) -> None:
        with (
            patch(
                "gale_shapley_algorithm._cli.prompts.Prompt.ask",
                side_effect=["Men", "Women", "Men", "Women"],
            ),
            patch(
                "gale_shapley_algorithm._cli.prompts.IntPrompt.ask",
                side_effect=[0, 2, 3, 3],
            ),
        ):
            result = prompt_random_config()
        assert result == ("Men", "Women", 3, 3)


# --- Unit tests for display.py ---


class TestDisplayResults:
    """Tests for display_results covering self-match, unmatched, and blocking pairs."""

    def test_self_matches_displayed(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Test that self-matches are shown."""
        from gale_shapley_algorithm._cli.display import display_results
        from gale_shapley_algorithm.result import MatchingResult, StabilityResult

        result = MatchingResult(rounds=1, matches={}, unmatched=[], self_matches=["Alice"], all_matched=False)
        stability = StabilityResult(is_stable=True, is_individually_rational=True, blocking_pairs=[])
        display_results("P", "R", result, stability)
        output = capsys.readouterr().out
        assert "(self)" in output

    def test_unmatched_displayed(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Test that unmatched persons are shown."""
        from gale_shapley_algorithm._cli.display import display_results
        from gale_shapley_algorithm.result import MatchingResult, StabilityResult

        result = MatchingResult(rounds=1, matches={}, unmatched=["Bob"], self_matches=[], all_matched=False)
        stability = StabilityResult(is_stable=True, is_individually_rational=True, blocking_pairs=[])
        display_results("P", "R", result, stability)
        output = capsys.readouterr().out
        assert "(unmatched)" in output

    def test_blocking_pairs_displayed(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Test that blocking pairs are shown."""
        from gale_shapley_algorithm._cli.display import display_results
        from gale_shapley_algorithm.result import MatchingResult, StabilityResult

        result = MatchingResult(rounds=1, matches={"A": "B"}, unmatched=[], self_matches=[], all_matched=True)
        stability = StabilityResult(is_stable=False, is_individually_rational=True, blocking_pairs=[("A", "C")])
        display_results("P", "R", result, stability)
        output = capsys.readouterr().out
        assert "Blocking pairs" in output

    def test_empty_preferences_shown(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Test that empty prefs display (none)."""
        from gale_shapley_algorithm._cli.display import display_preferences

        display_preferences("P", "R", {"Alice": []}, {"Bob": ["Alice"]})
        output = capsys.readouterr().out
        assert "(none)" in output


# --- Unit tests for app.py internals ---


class TestGenerateRandomPreferences:
    """Tests for _generate_random_preferences."""

    def test_same_first_letter(self) -> None:
        """When side names start with same letter, use full names."""
        from gale_shapley_algorithm._cli.app import _generate_random_preferences

        p_prefs, r_prefs = _generate_random_preferences("Cats", "Cows", 2, 2)
        p_names = list(p_prefs.keys())
        r_names = list(r_prefs.keys())
        assert all(n.startswith("cats_") for n in p_names)
        assert all(n.startswith("cows_") for n in r_names)

    def test_different_first_letter(self) -> None:
        """When side names start with different letters, use first letter."""
        from gale_shapley_algorithm._cli.app import _generate_random_preferences

        p_prefs, r_prefs = _generate_random_preferences("Men", "Women", 2, 2)
        p_names = list(p_prefs.keys())
        r_names = list(r_prefs.keys())
        assert all(n.startswith("m_") for n in p_names)
        assert all(n.startswith("w_") for n in r_names)


class TestRunMatching:
    """Tests for _run_matching."""

    def test_basic(self) -> None:
        """Basic matching with partial preferences."""
        from gale_shapley_algorithm._cli.app import _run_matching

        result, stability = _run_matching(
            {"A": ["X"]},
            {"X": ["A"]},
        )
        assert result.matches == {"A": "X"}
        assert stability.is_stable

    def test_partial_preferences_auto_appends(self) -> None:
        """Unlisted persons are auto-appended after self."""
        from gale_shapley_algorithm._cli.app import _run_matching

        result, stability = _run_matching(
            {"A": ["X"], "B": ["Y"]},
            {"X": ["A"], "Y": ["B"]},
        )
        assert result.matches
        assert stability.is_stable

    def test_complete_preferences(self) -> None:
        """All persons on other side listed — tests branch where append is skipped."""
        from gale_shapley_algorithm._cli.app import _run_matching

        result, stability = _run_matching(
            {"A": ["X", "Y"], "B": ["Y", "X"]},
            {"X": ["A", "B"], "Y": ["B", "A"]},
        )
        assert result.matches
        assert stability.is_stable

    def test_asymmetric_more_proposers(self) -> None:
        """With more proposers than responders, some must self-match or go unmatched."""
        from gale_shapley_algorithm._cli.app import _run_matching

        result, _ = _run_matching(
            {"A": ["X"], "B": ["X"], "C": ["X"]},
            {"X": ["A", "B", "C"]},
        )
        total = len(result.matches) + len(result.self_matches) + len(result.unmatched)
        assert total >= 3
