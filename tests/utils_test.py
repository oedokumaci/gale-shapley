import logging
from typing import Generator

import pytest
from pytest import LogCaptureFixture

from gale_shapley.config_parser import YAMLConfig
from gale_shapley.utils import LOG_PATH, log_config_info, timer_decorator


@pytest.mark.parametrize(
    "level,msg",
    [
        (logging.INFO, "info"),
        (logging.WARNING, "warning"),
        (logging.ERROR, "error"),
        (logging.CRITICAL, "critical"),
    ],
)
def test_init_logger(
    logger_fixture: None, caplog: Generator[LogCaptureFixture, None, None], level, msg
) -> None:
    logger_fixture
    logging.log(level, msg)

    # Assert that the log file was created in the correct directory
    log_file_path = LOG_PATH / "pytest_test.log"
    assert log_file_path.is_file()

    # Assert that the correct logs were produced
    assert caplog.record_tuples[-1] == ("root", level, msg)


def test_log_config_info(
    caplog: Generator[LogCaptureFixture, None, None],
    valid_yaml_config_input: dict,
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


def test_timer_decorator(caplog: Generator[LogCaptureFixture, None, None]) -> None:
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
