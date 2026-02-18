"""Test fixtures for the Gale-Shapley algorithm."""

import logging
from collections.abc import Generator
from typing import Final

import pytest

from gale_shapley.algorithm import Algorithm
from gale_shapley.person import Proposer, Responder


@pytest.fixture(autouse=True)
def _clean_logger() -> Generator[None, None, None]:
    """Remove all logging handlers before/after each test to prevent interference."""
    logger = logging.getLogger()
    logger.handlers.clear()
    logger.setLevel(logging.WARNING)
    yield
    for handler in logger.handlers[:]:
        handler.close()
    logger.handlers.clear()
    logger.setLevel(logging.WARNING)


# --- Person fixtures (function-scoped for isolation) ---


@pytest.fixture
def m_1_fix() -> Proposer:
    return Proposer("m_1", "man")


@pytest.fixture
def m_2_fix() -> Proposer:
    return Proposer("m_2", "man")


@pytest.fixture
def w_1_fix() -> Responder:
    return Responder("w_1", "woman")


@pytest.fixture
def w_2_fix() -> Responder:
    return Responder("w_2", "woman")


@pytest.fixture
def deterministic_proposers_and_responders(
    m_1_fix: Proposer, m_2_fix: Proposer, w_1_fix: Responder, w_2_fix: Responder
) -> tuple[list[Proposer], list[Responder]]:
    """Create proposers and responders with deterministic preferences.

       m_1 m_2 w_1 w_2
       --- --- --- ---
    1. w_1 w_1 m_1 m_2
    2. w_2 m_2 m_2 m_1
    3. m_1     w_1 w_2
    """
    proposers = [m_1_fix, m_2_fix]
    responders = [w_1_fix, w_2_fix]

    proposers[0].preferences = (responders[0], responders[1], proposers[0])
    proposers[1].preferences = (responders[0], proposers[1], responders[1])
    responders[0].preferences = (proposers[0], proposers[1], responders[0])
    responders[1].preferences = (proposers[1], proposers[0], responders[1])

    return proposers, responders


# Backward-compatible alias
@pytest.fixture
def create_deterministic_proposers_and_responders_fix(
    deterministic_proposers_and_responders: tuple[list[Proposer], list[Responder]],
) -> tuple[list[Proposer], list[Responder]]:
    return deterministic_proposers_and_responders


# --- Config fixtures (require CLI extras) ---


@pytest.fixture
def valid_yaml_config_input() -> dict:
    """Valid YAML config for random mode."""
    return {
        "proposer_side_name": "men",
        "responder_side_name": "women",
        "preference_type": "random",
        "number_of_proposers": 4,
        "number_of_responders": 5,
        "log_file_name": "simulation.log",
        "proposers": {
            "m1": ["w1", "w3"],
            "m2": ["w3", "w2"],
            "m3": ["w2", "w1", "w5"],
            "m4": [],
        },
        "responders": {
            "w1": ["m3"],
            "w2": ["m1", "m3", "m4"],
            "w3": ["m1", "m2"],
            "w4": [],
            "w5": ["m2"],
        },
    }


@pytest.fixture
def valid_input_yaml_config() -> dict:
    """Valid YAML config for input mode."""
    return {
        "proposer_side_name": "men",
        "responder_side_name": "women",
        "preference_type": "input",
        "number_of_proposers": 2,
        "number_of_responders": 2,
        "log_file_name": "test.log",
        "proposers": {
            "will": ["april", "summer"],
            "hampton": ["summer"],
        },
        "responders": {
            "april": ["will"],
            "summer": ["will", "hampton"],
        },
    }


# --- Algorithm fixtures ---


@pytest.fixture
def ran_algorithm_fix(
    deterministic_proposers_and_responders: tuple[list[Proposer], list[Responder]],
) -> Algorithm:
    """Algorithm that has been run to completion."""
    proposers, responders = deterministic_proposers_and_responders
    algo = Algorithm(proposers, responders)
    algo.execute()
    return algo


# --- CLI Simulator fixtures ---


@pytest.fixture
def sim_random_test_input_fix(request: pytest.FixtureRequest):
    """Create CLI Simulator objects with various random configs."""
    from gale_shapley._cli.config import YAMLConfig
    from gale_shapley._cli.simulator import Simulator

    num_proposers, num_responders = request.param
    mock_config: Final[dict] = {
        "proposer_side_name": "man",
        "responder_side_name": "woman",
        "number_of_proposers": num_proposers,
        "number_of_responders": num_responders,
        "preference_type": "Random",
        "log_file_name": "test_logs.log",
        "proposers": {},
        "responders": {},
    }
    return Simulator(YAMLConfig.model_validate(mock_config))


@pytest.fixture
def sim_input_mode_fix(valid_input_yaml_config: dict):
    """CLI Simulator with input preference config."""
    from gale_shapley._cli.config import YAMLConfig
    from gale_shapley._cli.simulator import Simulator

    return Simulator(YAMLConfig.model_validate(valid_input_yaml_config))


# --- Logger fixture ---


@pytest.fixture
def logger_fixture() -> Generator[None, None, None]:
    from gale_shapley._cli.logging import LOG_PATH, init_logger

    log_file_path = LOG_PATH / "pytest_test.log"
    init_logger(log_file_path.name)
    yield
    logger = logging.getLogger()
    for handler in logger.handlers:
        handler.close()
    log_file_path.unlink(missing_ok=True)
