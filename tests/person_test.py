"""Tests for the person module."""

from typing import ClassVar

import pytest

from gale_shapley.person import Proposer, Responder


class TestPerson:
    """Test class for Person base class functionality."""

    # Class variables for test data
    proposers: ClassVar[list[Proposer]]
    responders: ClassVar[list[Responder]]
    persons: ClassVar[list[Responder | Proposer]]
    m_1: ClassVar[Proposer]
    m_2: ClassVar[Proposer]
    w_1: ClassVar[Responder]
    w_2: ClassVar[Responder]

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

    def test_is_acceptable(self) -> None:
        """Test that is_acceptable works correctly.

        Preferences of proposers and responders:
           m_1 m_2 w_1 w_2
           --- --- --- ---
        1. w_1 w_1 m_1 m_2
        2. w_2 m_2 m_2 m_1
        3. m_1     w_1 w_2
        """
        # Test proposer preferences
        assert self.m_1.is_acceptable(self.w_1)
        assert self.m_1.is_acceptable(self.w_2)
        assert self.m_1.is_acceptable(self.m_1)
        assert self.m_2.is_acceptable(self.w_1)
        assert self.m_2.is_acceptable(self.m_2)
        assert not self.m_2.is_acceptable(self.w_2)

        # Test responder preferences
        assert self.w_1.is_acceptable(self.m_1)
        assert self.w_1.is_acceptable(self.m_2)
        assert self.w_1.is_acceptable(self.w_1)
        assert self.w_2.is_acceptable(self.m_2)
        assert self.w_2.is_acceptable(self.m_1)
        assert self.w_2.is_acceptable(self.w_2)

    def test_is_matched(self) -> None:
        """Test that is_matched property works correctly."""
        # Initially no one is matched
        for person in self.persons:
            assert not person.is_matched

        # Test matching
        self.m_1.match = self.w_1
        self.w_1.match = self.m_1
        assert self.m_1.is_matched
        assert self.w_1.is_matched

        # Test unmatching
        self.m_1.is_matched = False
        assert not self.m_1.is_matched
        assert self.m_1.match is None

        # Test invalid setting
        with pytest.raises(ValueError):
            self.m_1.is_matched = True
