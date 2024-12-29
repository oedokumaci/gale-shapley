"""Test fixtures for the Gale-Shapley algorithm."""

import logging
import random
from collections.abc import Generator
from typing import Final

import pytest

from gale_shapley.config import YAMLConfig, YAMLConfigDict
from gale_shapley.person import Proposer, Responder
from gale_shapley.simulator import Simulator
from gale_shapley.utils import LOG_PATH, init_logger


@pytest.fixture(scope="class")
def m_1_fix() -> Proposer:
    """Pytest fixture for proposer m_1."""
    return Proposer("m_1", "man")


@pytest.fixture(scope="class")
def m_2_fix() -> Proposer:
    """Pytest fixture for proposer m_2."""
    return Proposer("m_2", "man")


@pytest.fixture(scope="class")
def w_1_fix() -> Responder:
    """Pytest fixture for responder w_1."""
    return Responder("w_1", "woman")


@pytest.fixture(scope="class")
def w_2_fix() -> Responder:
    """Pytest fixture for responder w_2."""
    return Responder("w_2", "woman")


@pytest.fixture(scope="class")
def create_deterministic_proposers_and_responders_fix(
    m_1_fix: Proposer, m_2_fix: Proposer, w_1_fix: Responder, w_2_fix: Responder
) -> tuple[list[Proposer], list[Responder]]:
    """Pytest fixture to create proposers and responders with following preferences.
       m_1 m_2 w_1 w_2
       --- --- --- ---
    1. w_1 w_1 m_1 m_2
    2. w_2 m_2 m_2 m_1
    3. m_1     w_1 w_2

    Args:
        m_1_fix (Proposer): conftest.py fixture
        m_2_fix (Proposer): conftest.py fixture
        w_1_fix (Responder): conftest.py fixture
        w_2_fix (Responder): conftest.py fixture

    Returns:
        tuple[list[Proposer], list[Responder]]: tuple of list of proposers and list of responders
    """
    proposers: list[Proposer] = [m_1_fix, m_2_fix]
    responders: list[Responder] = [w_1_fix, w_2_fix]

    proposers[0].preferences = (responders[0], responders[1], proposers[0])
    proposers[1].preferences = (responders[0], proposers[1], responders[1])
    responders[0].preferences = (proposers[0], proposers[1], responders[0])
    responders[1].preferences = (proposers[1], proposers[0], responders[1])

    return proposers, responders


@pytest.fixture(
    params=[(random.randint(1, 20), random.randint(1, 20)) for _ in range(20)]
)
def sim_random_test_input_fix(request: pytest.FixtureRequest) -> Simulator:
    """Pytest fixture to create 20 Simulator objects.
    There are between 1 to 20 (not necessarily equal) number of men and women.
    Preferences are also randomly generated.
    Pytest fixture request is used to pass parameters to the fixture.

    Args:
        request (pytest.FixtureRequest): pytest fixture request

    Returns:
        Simulator: A simulator instance with random configuration
    """
    num_proposers, num_responders = request.param

    mock_config: Final[YAMLConfigDict] = {
        "proposer_side_name": "man",
        "responder_side_name": "woman",
        "number_of_proposers": num_proposers,
        "number_of_responders": num_responders,
        "preference_type": "Random",
        "log_file_name": "test_logs.log",
        "proposers": {},
        "responders": {},
    }
    return Simulator(YAMLConfig.parse_obj(mock_config))


@pytest.fixture
def valid_yaml_config_input() -> dict:
    """Returns a valid YAML configuration dictionary for testing.

    Returns:
        dict: A valid configuration dictionary
    """
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


@pytest.fixture(scope="package")
def logger_fixture() -> Generator[None, None, None]:
    log_file_path = LOG_PATH / "pytest_test.log"
    init_logger(log_file_path.name)
    yield
    logger = logging.getLogger()
    for handler in logger.handlers:  # close all handlers, Windows fix
        handler.close()
    log_file_path.unlink()
