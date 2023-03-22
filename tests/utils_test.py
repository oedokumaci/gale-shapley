import logging
from typing import Generator

from pytest import LogCaptureFixture

from gale_shapley.config_parser import YAMLConfig
from gale_shapley.utils import LOG_PATH, init_logger, log_config_info, timer_decorator


def test_init_logger(caplog: Generator[LogCaptureFixture, None, None]) -> None:
    log_file_path = LOG_PATH / "pytest_test.log"
    init_logger(log_file_path.name)

    # Assert that the log file was created in the correct directory
    assert log_file_path.is_file()

    logging.debug("test")

    # Assert that the correct logs were produced
    assert caplog.record_tuples == [
        ("root", logging.INFO, f"Path to log file: {log_file_path.resolve()}"),
        ("root", logging.DEBUG, "test"),
    ]


def test_unlink_log_file() -> None:
    log_file_path = LOG_PATH / "pytest_test.log"
    log_file_path.unlink()
    assert not log_file_path.exists()


def test_log_config_info(
    caplog: Generator[LogCaptureFixture, None, None], valid_yaml_config_input: dict
) -> None:
    # Set up a YAMLConfig object with some test data
    config_input = YAMLConfig(**valid_yaml_config_input)

    # Call the function and check that the correct logs were produced
    log_config_info(config_input)
    assert caplog.record_tuples == [
        ("root", logging.INFO, "Parsing config.yaml is complete."),
        ("root", logging.INFO, "Proposer side name: men, Responder side name: women"),
        ("root", logging.INFO, "Number of proposers: 4, Number of responders: 5"),
        ("root", logging.INFO, "Preference type: random"),
    ]


def test_timer_decorator(caplog) -> None:
    # Define a test function that takes some time to execute
    @timer_decorator
    def test_function() -> str:
        for _ in range(1000000):
            pass
        return "done"

    # Call the function and check that the correct logs were produced
    result = test_function()
    assert result == "done"
    assert caplog.record_tuples[0][2].startswith(
        "Method 'test_function' of module 'tests.utils_test' executed in "
    )
