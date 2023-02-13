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
    algorithm = Algorithm(proposers, responders)
    assert proposers[0].last_proposal is None
    assert proposers[1].last_proposal is None
    assert proposers[0].next_proposal == responders[0]
    assert proposers[1].next_proposal == responders[0]
    assert responders[0].current_proposals is None
    assert responders[1].current_proposals is None
    algorithm.proposers_propose()
    assert proposers[0].last_proposal is responders[0]
    assert proposers[1].last_proposal is responders[0]
    assert proposers[0].next_proposal == responders[1]
    assert proposers[1].next_proposal == proposers[1]
    assert responders[0].current_proposals == [proposers[0], proposers[1]]
    assert responders[1].current_proposals is None
    algorithm.responders_respond()
    assert responders[0].current_proposals is None
    assert responders[1].current_proposals is None
    assert proposers[0].match == responders[0]
    assert responders[0].match == proposers[0]
    assert proposers[1].match is None
    assert responders[1].match is None
    assert not algorithm.terminate()
