from gale_shapley.simulator import Simulator


def test_stability(sim_random_test_input_fix: Simulator) -> None:
    """Checks resulting match stability by using Simulator simulate method.
    This is 20 random tests.

    Args:
        sim_random_test_input_fix (Simulator): conftest.py fixture
    """
    sim_random_test_input_fix.number_of_simulations = 1
    sim_random_test_input_fix.simulate(
        print_all_preferences=False, compact=False, report_matches=False
    )
    assert sim_random_test_input_fix.is_stable()
