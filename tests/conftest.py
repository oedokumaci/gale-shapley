import random

import pytest

from gale_shapley.person import Proposer, Responder
from gale_shapley.simulator import Simulator


@pytest.fixture
def m_1() -> Proposer:
    """Pytest fixture for proposer m_1."""
    return Proposer("m_1", "man")


@pytest.fixture
def m_2() -> Proposer:
    """Pytest fixture for proposer m_2."""
    return Proposer("m_2", "man")


@pytest.fixture
def w_1() -> Responder:
    """Pytest fixture for responder w_1."""
    return Responder("w_1", "woman")


@pytest.fixture
def w_2() -> Responder:
    """Pytest fixture for responder w_2."""
    return Responder("w_2", "woman")


@pytest.fixture
def create_deterministic_proposers_and_responders(
    m_1: Proposer, m_2: Proposer, w_1: Responder, w_2: Responder
) -> tuple[list[Proposer], list[Responder]]:
    """Pytest fixture to create proposers and responders with following preferences.
       m_1 m_2 w_1 w_2
       --- --- --- ---
    1. w_1 w_1 m_1 m_2
    2. w_2 m_2 m_2 m_1
    3. m_1     w_1 w_2

    Args:
        m_1 (Proposer): conftest.py fixture
        m_2 (Proposer): conftest.py fixture
        w_1 (Responder): conftest.py fixture
        w_2 (Responder): conftest.py fixture

    Returns:
        tuple[list[Proposer], list[Responder]]: tuple of list of proposers and list of responders
    """
    proposers: list[Proposer]
    responders: list[Responder]
    proposers, responders = [m_1, m_2], [w_1, w_2]
    proposers[0].preferences = [responders[0], responders[1], proposers[0]]
    proposers[1].preferences = [responders[0], proposers[1], responders[1]]
    responders[0].preferences = [proposers[0], proposers[1], responders[0]]
    responders[1].preferences = [proposers[1], proposers[0], responders[1]]
    return proposers, responders


@pytest.fixture(
    params=[(random.randint(1, 20), random.randint(1, 20)) for _ in range(20)]
)
def sim_random_test_input(request: pytest.FixtureRequest) -> Simulator:
    """Pytest fixture to create 20 Simulator objects.
    There are between 1 to 20 (not necessarily equal) number of men and women.
    Preferences are also randomly generated.
    Pytest fixture request is used to pass parameters to the fixture.

    Args:
        request (pytest.FixtureRequest): pytest fixture request

    Returns:
        Simulator:
    """
    number_of_proposers: int
    number_of_responders: int
    number_of_proposers, number_of_responders = request.param
    sim = Simulator("man", "woman", number_of_proposers, number_of_responders, "random")
    return sim