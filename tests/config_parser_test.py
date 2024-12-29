"""Tests for the config parser module."""

from typing import Any

import pytest

from gale_shapley.config import YAMLConfig, side_swap


def test_valid_yaml_input(valid_yaml_config_input: dict[str, Any]) -> None:
    """Test that valid YAML input is parsed correctly.

    Args:
        valid_yaml_config_input: Fixture providing valid YAML config
    """
    config = YAMLConfig.parse_obj(valid_yaml_config_input)
    assert config.proposer_side_name == "men"
    assert config.responder_side_name == "women"
    assert config.preference_type == "random"
    assert config.number_of_proposers == 4
    assert config.number_of_responders == 5
    assert config.log_file_name == "simulation.log"
    assert config.proposers == {
        "m1": ["w1", "w3"],
        "m2": ["w3", "w2"],
        "m3": ["w2", "w1", "w5"],
        "m4": [],
    }
    assert config.responders == {
        "w1": ["m3"],
        "w2": ["m1", "m3", "m4"],
        "w3": ["m1", "m2"],
        "w4": [],
        "w5": ["m2"],
    }


def test_valid_side_swap(valid_yaml_config_input: dict[str, Any]) -> None:
    """Test that side swap works correctly.

    Args:
        valid_yaml_config_input: Fixture providing valid YAML config
    """
    config = YAMLConfig.parse_obj(valid_yaml_config_input)
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
    assert config.responders == {
        "m1": ["w1", "w3"],
        "m2": ["w3", "w2"],
        "m3": ["w2", "w1", "w5"],
        "m4": [],
    }


@pytest.mark.parametrize(
    "invalid_input,expected_error",
    [
        (
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
            ValueError,
        ),
        (
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
            ValueError,
        ),
        (
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
            ValueError,
        ),
        (
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
            ValueError,
        ),
        (
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
            ValueError,
        ),
        (
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
            ValueError,
        ),
    ],
)
def test_invalid_yaml_input(
    invalid_input: dict[str, Any], expected_error: type[Exception]
) -> None:
    """Test that invalid YAML input raises appropriate errors.

    Args:
        invalid_input: Invalid YAML input
        expected_error: Expected error type
    """
    with pytest.raises(expected_error):
        YAMLConfig.parse_obj(invalid_input)
