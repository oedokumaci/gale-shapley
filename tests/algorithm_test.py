from gale_shapley.algorithm import Algorithm
from gale_shapley.person import Proposer, Responder


def test_propose_respond_terminate(
    create_deterministic_proposers_and_responders: tuple[
        list[Proposer], list[Responder]
    ]
) -> None:
    """Checks individual methods contribute to algorithm run method using deterministic input.

    Args:
        create_deterministic_proposers_and_responders (tuple[list[Proposer], list[Responder]]): conftest.py fixture
    """
    proposers: list[Proposer]
    responders: list[Responder]
    proposers, responders = create_deterministic_proposers_and_responders
    m_1, m_2 = proposers
    w_1, w_2 = responders
    algorithm = Algorithm(proposers, responders)
    # Preferences of proposers and responders:
    #    m_1 m_2 w_1 w_2
    #    --- --- --- ---
    # 1. w_1 w_1 m_1 m_2
    # 2. w_2 m_2 m_2 m_1
    # 3. m_1     w_1 w_2
    assert m_1.last_proposal is None
    assert m_2.last_proposal is None
    assert m_1.next_proposal == w_1
    assert m_2.next_proposal == w_1
    assert w_1.current_proposals is None
    assert w_2.current_proposals is None
    algorithm.proposers_propose()
    assert m_1.last_proposal == w_1
    assert m_2.last_proposal == w_1
    assert m_1.next_proposal == w_2
    assert m_2.next_proposal == m_2
    assert w_1.current_proposals == [m_1, m_2]
    assert w_2.current_proposals is None
    algorithm.responders_respond()
    assert w_1.current_proposals is None
    assert w_2.current_proposals is None
    assert m_1.match == w_1
    assert w_1.match == m_1
    assert m_2.match is None
    assert w_2.match is None
    assert not algorithm.terminate()
