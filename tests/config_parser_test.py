import pytest
from pydantic.error_wrappers import ValidationError

from gale_shapley.config_parser import YAMLConfig, side_swap


def test_valid_yaml_input(valid_yaml_config_input: dict) -> None:
    config = YAMLConfig(**valid_yaml_config_input)
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


def test_valid_side_swap(valid_yaml_config_input: dict) -> None:
    config = YAMLConfig(**valid_yaml_config_input)
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
    "invalid_input,error_type",
    [
        ({"preference_type": "invalid"}, ValueError),
        ({"number_of_proposers": -1}, ValueError),
        ({"number_of_responders": -1}, ValueError),
        ({"log_file_name": ""}, ValueError),
        ({"proposer_side_name": []}, ValidationError),
        ({"responder_side_name": []}, ValidationError),
    ],
)
def test_invalid_yaml_input(
    valid_yaml_config_input: dict, invalid_input: dict, error_type: type
) -> None:
    with pytest.raises(error_type):
        input_data = {**valid_yaml_config_input, **invalid_input}
        YAMLConfig(**input_data)
