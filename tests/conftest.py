import pytest

from gale_shapley.person import Proposer, Responder
from gale_shapley.simulator import Simulator


@pytest.fixture(scope="module")
def m_1() -> Proposer:
    return Proposer("m_1", "man")


@pytest.fixture(scope="module")
def m_2() -> Proposer:
    return Proposer("m_2", "man")


@pytest.fixture(scope="module")
def w_1() -> Responder:
    return Responder("w_1", "woman")


@pytest.fixture(scope="module")
def w_2() -> Responder:
    return Responder("w_2", "woman")


@pytest.fixture(scope="module")
def create_proposers_and_responders(
    m_1: Proposer, m_2: Proposer, w_1: Responder, w_2: Responder
) -> tuple[list[Proposer], list[Responder]]:
    proposers: list[Proposer]
    responders: list[Responder]
    proposers, responders = [m_1, m_2], [w_1, w_2]
    proposers[0].preferences = [responders[0], responders[1], proposers[0]]
    proposers[1].preferences = [responders[1], responders[0], proposers[1]]
    responders[0].preferences = [proposers[0], proposers[1], responders[0]]
    responders[1].preferences = [proposers[1], proposers[0], responders[1]]
    return proposers, responders


@pytest.fixture(scope="module")
def create_random_proposers_and_responders() -> tuple[list[Proposer], list[Responder]]:
    return Simulator.create_random_proposers_and_responders(5, 5)
