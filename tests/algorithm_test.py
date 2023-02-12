from gale_shapley.algorithm import Algorithm
from gale_shapley.person import Proposer, Responder


def test_unmatched_and_awaiting_after_run(
    create_proposers_and_responders: tuple[list[Proposer], list[Responder]]
) -> None:
    proposers: list[Proposer]
    responders: list[Responder]
    proposers, responders = create_proposers_and_responders
    algorithm = Algorithm(proposers, responders)
    algorithm.run()
    assert algorithm.unmatched_proposers == []
    assert algorithm.awaiting_to_respond_responders == []
    assert proposers[0].match == responders[0]
    assert proposers[1].match == responders[1]
