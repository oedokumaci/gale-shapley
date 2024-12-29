"""Tests for the simulator module."""

from typing import ClassVar

import pytest

from gale_shapley.simulator import Simulator


class TestSimulator:
    """Test class for Simulator functionality."""

    sim: ClassVar[Simulator]

    @pytest.fixture(autouse=True)
    def set_simulator_fix(self, sim_random_test_input_fix: Simulator) -> None:
        """Set up test data with random simulator input.

        Args:
            sim_random_test_input_fix: Fixture providing random simulator input
        """
        self.__class__.sim = sim_random_test_input_fix

    def test_simulate(self) -> None:
        """Test that simulation runs correctly."""
        # Run simulation
        self.sim.simulate(
            print_all_preferences=False,
            compact=True,
            report_matches=False,
        )

        # Check that results were collected
        assert len(self.sim.results) == self.sim.number_of_simulations

        # Check that all matches are stable
        for algorithm in self.sim.results:
            assert all(proposer.is_matched for proposer in algorithm.proposers)
