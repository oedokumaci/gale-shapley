"""Tests for the Gale-Shapley algorithm module."""

from typing import ClassVar

import pytest

from gale_shapley.algorithm import Algorithm
from gale_shapley.person import Proposer, Responder


class TestProposeRespondTerminate:
    """Test class for propose, respond, and terminate methods."""

    # Class variables for test data
    proposers: ClassVar[list[Proposer]]
    responders: ClassVar[list[Responder]]
    persons: ClassVar[list[Responder | Proposer]]
    m_1: ClassVar[Proposer]
    m_2: ClassVar[Proposer]
    w_1: ClassVar[Responder]
    w_2: ClassVar[Responder]
    algorithm: ClassVar[Algorithm]

    @pytest.fixture(autouse=True)
    def set_proposers_and_responders_fix(
        self,
        create_deterministic_proposers_and_responders_fix: tuple[
            list[Proposer], list[Responder]
        ],
    ) -> None:
        """Set up test data with deterministic proposers and responders.

        Args:
            create_deterministic_proposers_and_responders_fix: Fixture providing proposers and responders
        """
        (
            self.__class__.proposers,
            self.__class__.responders,
        ) = create_deterministic_proposers_and_responders_fix
        self.__class__.persons = self.proposers + self.responders
        self.__class__.m_1, self.__class__.m_2 = self.proposers
        self.__class__.w_1, self.__class__.w_2 = self.responders
        self.__class__.algorithm = Algorithm(self.proposers, self.responders)

    def test_proposers_propose(self) -> None:
        """Test that proposers propose correctly.

        Preferences of proposers and responders:
           m_1 m_2 w_1 w_2
           --- --- --- ---
        1. w_1 w_1 m_1 m_2
        2. w_2 m_2 m_2 m_1
        3. m_1     w_1 w_2
        """
        self.algorithm.proposers_propose()

        # Check last proposals
        assert self.m_1.last_proposal == self.w_1
        assert self.m_2.last_proposal == self.w_1

        # Check next proposals
        assert self.m_1.next_proposal == self.w_2
        assert self.m_2.next_proposal == self.m_2

        # Check current proposals
        assert self.w_1.current_proposals == [self.m_1, self.m_2]
        assert not self.w_2.current_proposals

    def test_responders_respond(self) -> None:
        """Test that responders respond correctly."""
        self.algorithm.responders_respond()

        # Check current proposals are cleared
        assert not self.w_1.current_proposals
        assert not self.w_2.current_proposals

        # Check matches
        assert self.m_1.match == self.w_1
        assert self.w_1.match == self.m_1
        assert not self.m_2.match
        assert not self.w_2.match

    def test_terminate(self) -> None:
        """Test that algorithm terminates correctly."""
        # Should not terminate initially
        assert not self.algorithm.terminate()

        # Run one round
        self.algorithm.proposers_propose()
        self.algorithm.responders_respond()

        # Should terminate after one round
        assert self.algorithm.terminate()
