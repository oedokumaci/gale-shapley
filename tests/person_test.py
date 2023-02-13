from gale_shapley.person import Proposer, Responder


def test_proposers_and_responders(
    create_deterministic_proposers_and_responders: tuple[
        list[Proposer], list[Responder]
    ]
) -> None:
    """Test proposers and responders.

    Args:
        create_deterministic_proposers_and_responders (tuple[ list[Proposer], list[Responder] ]): conftest.py fixture
    """
    proposers: list[Proposer]
    responders: list[Responder]
    proposers, responders = create_deterministic_proposers_and_responders
    persons = proposers + responders
    m_1, m_2 = proposers
    w_1, w_2 = responders
    # Preferences of proposers and responders:
    #    m_1 m_2 w_1 w_2
    #    --- --- --- ---
    # 1. w_1 w_1 m_1 m_2
    # 2. w_2 m_2 m_2 m_1
    # 3. m_1     w_1 w_2
    assert m_1.is_acceptable(w_1)
    assert not m_2.is_acceptable(w_2)
    for person in persons:
        assert person.is_acceptable(person)
        assert not person.is_matched
    assert m_1.acceptable_to_propose == (w_1, w_2, m_1)
    assert m_2.acceptable_to_propose == (w_1, m_2)
    for proposer in proposers:
        proposer.propose()
    assert m_1.last_proposal == w_1
    assert m_1.next_proposal == w_2
    assert m_2.last_proposal == w_1
    assert m_2.next_proposal == m_2
    assert w_1.current_proposals == [m_1, m_2]
    assert w_2.current_proposals is None
    assert w_1.awaiting_to_respond
    assert not w_2.awaiting_to_respond
    assert w_1.acceptable_proposals == [m_1, m_2]
    assert w_2.acceptable_proposals == []
    for responder in responders:
        responder.respond()
    assert w_1.match == m_1
    assert m_1.match == w_1
    assert not m_2.is_matched
    assert not w_2.is_matched
    assert w_1._most_preferred([m_1, m_2]) == m_1
    assert w_2._most_preferred([m_1, m_2]) == m_2
