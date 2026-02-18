"""Tests for the CLI simulator module."""

import logging

import pytest

from gale_shapley.person import Proposer, Responder


class TestSimulatorProperties:
    """Tests for CLI Simulator properties."""

    def test_persons_property(self, sim_input_mode_fix) -> None:
        sim_input_mode_fix.proposers, sim_input_mode_fix.responders = sim_input_mode_fix.create_objects()
        assert sim_input_mode_fix.persons == (sim_input_mode_fix.proposers + sim_input_mode_fix.responders)


class TestCreateObjects:
    """Tests for create_objects."""

    def test_random_mode_different_first_letters(self) -> None:
        from gale_shapley._cli.config import YAMLConfig
        from gale_shapley._cli.simulator import Simulator

        config = YAMLConfig.model_validate(
            {
                "proposer_side_name": "men",
                "responder_side_name": "women",
                "preference_type": "random",
                "number_of_proposers": 3,
                "number_of_responders": 2,
                "log_file_name": "test.log",
                "proposers": {},
                "responders": {},
            }
        )
        sim = Simulator(config)
        proposers, responders = sim.create_objects()
        assert len(proposers) == 3
        assert len(responders) == 2
        assert proposers[0].name.startswith("m")
        assert responders[0].name.startswith("w")
        for p in proposers:
            assert len(p.preferences) == len(responders) + 1

    def test_random_mode_same_first_letters(self) -> None:
        """When side names start with same letter, use full names."""
        from gale_shapley._cli.config import YAMLConfig
        from gale_shapley._cli.simulator import Simulator

        config = YAMLConfig.model_validate(
            {
                "proposer_side_name": "cats",
                "responder_side_name": "cows",
                "preference_type": "random",
                "number_of_proposers": 2,
                "number_of_responders": 2,
                "log_file_name": "test.log",
                "proposers": {},
                "responders": {},
            }
        )
        sim = Simulator(config)
        proposers, responders = sim.create_objects()
        assert proposers[0].name.startswith("cats")
        assert responders[0].name.startswith("cows")

    def test_input_mode_complete_preferences(self, sim_input_mode_fix) -> None:
        proposers, responders = sim_input_mode_fix.create_objects()
        assert len(proposers) == 2
        assert len(responders) == 2
        for p in proposers:
            assert len(p.preferences) > 0
        for r in responders:
            assert len(r.preferences) > 0

    def test_input_mode_partial_preferences(self) -> None:
        """Partial preferences should be filled in with remaining persons + self."""
        from gale_shapley._cli.config import YAMLConfig
        from gale_shapley._cli.simulator import Simulator

        config = YAMLConfig.model_validate(
            {
                "proposer_side_name": "men",
                "responder_side_name": "women",
                "preference_type": "input",
                "number_of_proposers": 2,
                "number_of_responders": 2,
                "log_file_name": "test.log",
                "proposers": {
                    "m1": ["w1"],
                    "m2": ["w2", "w1"],
                },
                "responders": {
                    "w1": ["m1"],
                    "w2": ["m2", "m1"],
                },
            }
        )
        sim = Simulator(config)
        proposers, responders = sim.create_objects()
        for p in proposers:
            assert len(p.preferences) == len(responders) + 1
        for r in responders:
            assert len(r.preferences) == len(proposers) + 1


class TestSimulate:
    """Tests for simulate method."""

    @pytest.mark.parametrize(
        "sim_random_test_input_fix",
        [(2, 2), (3, 3), (1, 3), (3, 1), (5, 5)],
        indirect=True,
    )
    def test_simulate_random(self, sim_random_test_input_fix) -> None:
        sim_random_test_input_fix.simulate(print_all_preferences=False, compact=True, report_matches=False)
        assert len(sim_random_test_input_fix.results) == sim_random_test_input_fix.number_of_simulations
        for algo in sim_random_test_input_fix.results:
            assert all(p.is_matched for p in algo.proposers)

    def test_simulate_with_all_options(self, caplog: pytest.LogCaptureFixture) -> None:
        from gale_shapley._cli.config import YAMLConfig
        from gale_shapley._cli.simulator import Simulator

        config = YAMLConfig.model_validate(
            {
                "proposer_side_name": "men",
                "responder_side_name": "women",
                "preference_type": "random",
                "number_of_proposers": 2,
                "number_of_responders": 2,
                "log_file_name": "test.log",
                "proposers": {},
                "responders": {},
            }
        )
        sim = Simulator(config)
        sim.number_of_simulations = 2
        with caplog.at_level(logging.INFO):
            sim.simulate(print_all_preferences=True, compact=True, report_matches=True)
        assert "Starting simulations" in caplog.text
        assert "Simulations ended" in caplog.text
        assert len(sim.results) == 2

    def test_simulate_with_report_only(self, caplog: pytest.LogCaptureFixture) -> None:
        from gale_shapley._cli.config import YAMLConfig
        from gale_shapley._cli.simulator import Simulator

        config = YAMLConfig.model_validate(
            {
                "proposer_side_name": "men",
                "responder_side_name": "women",
                "preference_type": "random",
                "number_of_proposers": 2,
                "number_of_responders": 2,
                "log_file_name": "test.log",
                "proposers": {},
                "responders": {},
            }
        )
        sim = Simulator(config)
        sim.number_of_simulations = 1
        with caplog.at_level(logging.INFO):
            sim.simulate(print_all_preferences=False, compact=False, report_matches=True)
        assert "Matching:" in caplog.text

    def test_simulate_input_mode(
        self,
        sim_input_mode_fix,
        caplog: pytest.LogCaptureFixture,
    ) -> None:
        sim_input_mode_fix.number_of_simulations = 1
        with caplog.at_level(logging.INFO):
            sim_input_mode_fix.simulate(print_all_preferences=False, report_matches=False)
        assert len(sim_input_mode_fix.results) == 1


class TestStability:
    """Tests for stability functions via the core stability module."""

    def _make_sim(self, proposers: list[Proposer], responders: list[Responder]):
        from gale_shapley._cli.simulator import Simulator

        sim = Simulator.__new__(Simulator)
        sim.proposers = proposers
        sim.responders = responders
        sim.config_input = None  # type: ignore[assignment]
        sim.results = []
        sim.number_of_simulations = 0
        return sim
