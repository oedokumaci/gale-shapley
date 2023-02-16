from __future__ import annotations

import pytest

from gale_shapley.person import Proposer, Responder


class TestProposerResponder:
    proposers: list[Proposer]
    responders: list[Responder]
    persons: list[Responder | Proposer]
    m_1: Proposer
    m_2: Proposer
    w_1: Responder
    w_2: Responder

    @pytest.fixture(autouse=True)
    def set_proposers_and_responders_fix(
        self,
        create_deterministic_proposers_and_responders_fix: tuple[
            list[Proposer], list[Responder]
        ],
    ) -> None:
        (
            self.__class__.proposers,
            self.__class__.responders,
        ) = create_deterministic_proposers_and_responders_fix
        self.__class__.persons = self.proposers + self.responders
        self.__class__.m_1, self.__class__.m_2 = self.proposers
        self.__class__.w_1, self.__class__.w_2 = self.responders

    # Preferences of proposers and responders:
    #    m_1 m_2 w_1 w_2
    #    --- --- --- ---
    # 1. w_1 w_1 m_1 m_2
    # 2. w_2 m_2 m_2 m_1
    # 3. m_1     w_1 w_2

    def test_is_acceptable(self) -> None:
        assert self.m_1.is_acceptable(self.w_1)
        assert not self.m_2.is_acceptable(self.w_2)
        for person in self.persons:
            assert person.is_acceptable(person)

    def test_is_matched(self) -> None:
        for person in self.persons:
            assert not person.is_matched

    def test_acceptable_to_propose(self) -> None:
        assert self.m_1.acceptable_to_propose == (self.w_1, self.w_2, self.m_1)
        assert self.m_2.acceptable_to_propose == (self.w_1, self.m_2)

    def test_propose(self) -> None:
        for proposer in self.proposers:
            proposer.propose()

    def test_last_proposal(self) -> None:
        assert self.m_1.last_proposal == self.w_1
        assert self.m_2.last_proposal == self.w_1

    def test_next_proposal(self) -> None:
        assert self.m_1.next_proposal == self.w_2
        assert self.m_2.next_proposal == self.m_2
