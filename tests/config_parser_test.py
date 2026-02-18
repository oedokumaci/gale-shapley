"""Tests for the CLI config parser module."""

import warnings
from typing import Any

import pytest

from gale_shapley._cli.config import YAMLConfig, side_swap


def test_valid_yaml_input(valid_yaml_config_input: dict[str, Any]) -> None:
    config = YAMLConfig.model_validate(valid_yaml_config_input)
    assert config.proposer_side_name == "men"
    assert config.responder_side_name == "women"
    assert config.preference_type == "random"
    assert config.number_of_proposers == 4
    assert config.number_of_responders == 5
    assert config.log_file_name == "simulation.log"


def test_valid_side_swap(valid_yaml_config_input: dict[str, Any]) -> None:
    config = YAMLConfig.model_validate(valid_yaml_config_input)
    side_swap(config)
    assert config.proposer_side_name == "women"
    assert config.responder_side_name == "men"
    assert config.number_of_proposers == 5
    assert config.number_of_responders == 4
    assert config.proposers == {
        "w1": ["m3"],
        "w2": ["m1", "m3", "m4"],
        "w3": ["m1", "m2"],
        "w4": [],
        "w5": ["m2"],
    }


@pytest.mark.parametrize(
    "invalid_input",
    [
        # Same side names
        {
            "proposer_side_name": "men",
            "responder_side_name": "men",
            "preference_type": "random",
            "number_of_proposers": 4,
            "number_of_responders": 5,
            "log_file_name": "simulation.log",
            "proposers": {},
            "responders": {},
        },
        # Invalid preference type
        {
            "proposer_side_name": "men",
            "responder_side_name": "women",
            "preference_type": "invalid",
            "number_of_proposers": 4,
            "number_of_responders": 5,
            "log_file_name": "simulation.log",
            "proposers": {},
            "responders": {},
        },
        # Negative proposers
        {
            "proposer_side_name": "men",
            "responder_side_name": "women",
            "preference_type": "random",
            "number_of_proposers": -1,
            "number_of_responders": 5,
            "log_file_name": "simulation.log",
            "proposers": {},
            "responders": {},
        },
        # Log file starts with /
        {
            "proposer_side_name": "men",
            "responder_side_name": "women",
            "preference_type": "random",
            "number_of_proposers": 4,
            "number_of_responders": 5,
            "log_file_name": "/simulation.log",
            "proposers": {},
            "responders": {},
        },
        # Log file without .log extension
        {
            "proposer_side_name": "men",
            "responder_side_name": "women",
            "preference_type": "random",
            "number_of_proposers": 4,
            "number_of_responders": 5,
            "log_file_name": "simulation",
            "proposers": {},
            "responders": {},
        },
        # Input mode with no proposers
        {
            "proposer_side_name": "men",
            "responder_side_name": "women",
            "preference_type": "input",
            "number_of_proposers": 4,
            "number_of_responders": 5,
            "log_file_name": "simulation.log",
            "proposers": {},
            "responders": {},
        },
    ],
)
def test_invalid_yaml_input(invalid_input: dict[str, Any]) -> None:
    with pytest.raises(ValueError):
        YAMLConfig.model_validate(invalid_input)


def test_input_preference_references_nonexistent_person() -> None:
    """Preference referencing a person not on the other side raises ValueError."""
    with pytest.raises(ValueError, match="not in"):
        YAMLConfig.model_validate(
            {
                "proposer_side_name": "men",
                "responder_side_name": "women",
                "preference_type": "input",
                "number_of_proposers": 1,
                "number_of_responders": 1,
                "log_file_name": "test.log",
                "proposers": {"m1": ["nonexistent"]},
                "responders": {"w1": ["m1"]},
            }
        )


def test_input_count_mismatch_warning() -> None:
    """Warning when number_of_proposers doesn't match actual count."""
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        YAMLConfig.model_validate(
            {
                "proposer_side_name": "men",
                "responder_side_name": "women",
                "preference_type": "input",
                "number_of_proposers": 99,
                "number_of_responders": 2,
                "log_file_name": "test.log",
                "proposers": {
                    "m1": ["w1", "w2"],
                    "m2": ["w2", "w1"],
                },
                "responders": {
                    "w1": ["m1", "m2"],
                    "w2": ["m2", "m1"],
                },
            }
        )
        assert any("does not match" in str(warning.message) for warning in w)


def test_valid_input_mode_complete(valid_input_yaml_config: dict) -> None:
    """Valid input mode config parses without error."""
    config = YAMLConfig.model_validate(valid_input_yaml_config)
    assert config.preference_type == "input"
    assert len(config.proposers) == 2
    assert len(config.responders) == 2
