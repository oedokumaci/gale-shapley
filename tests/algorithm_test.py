from __future__ import annotations

import pytest

from gale_shapley.algorithm import Algorithm
from gale_shapley.person import Proposer, Responder


class TestProposeRespondTerminate:
    proposers: list[Proposer]
    responders: list[Responder]
    persons: list[Responder | Proposer]
    m_1: Proposer
    m_2: Proposer
    w_1: Responder
    w_2: Responder
    algorithm: Algorithm

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
        self.__class__.algorithm = Algorithm(self.proposers, self.responders)

    # Preferences of proposers and responders:
    #    m_1 m_2 w_1 w_2
    #    --- --- --- ---
    # 1. w_1 w_1 m_1 m_2
    # 2. w_2 m_2 m_2 m_1
    # 3. m_1     w_1 w_2

    def test_proposers_propose(self) -> None:
        self.algorithm.proposers_propose()
        assert self.m_1.last_proposal == self.w_1
        assert self.m_2.last_proposal == self.w_1
        assert self.m_1.next_proposal == self.w_2
        assert self.m_2.next_proposal == self.m_2
        assert self.w_1.current_proposals == [self.m_1, self.m_2]
        assert self.w_2.current_proposals is None

    def test_responders_respond(self) -> None:
        self.algorithm.responders_respond()
        assert self.w_1.current_proposals is None
        assert self.w_2.current_proposals is None
        assert self.m_1.match == self.w_1
        assert self.w_1.match == self.m_1
        assert self.m_2.match is None
        assert self.w_2.match is None

    def test_terminate(self) -> None:
        assert not self.algorithm.terminate()
        self.algorithm.proposers_propose()
        self.algorithm.responders_respond()
        assert self.algorithm.terminate()
