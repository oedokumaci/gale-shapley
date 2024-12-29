"""Tests for the utils module."""

import logging
from typing import Final

from gale_shapley.config import YAMLConfig
from gale_shapley.utils import LOG_PATH, init_logger, log_config_info, timer_decorator


def test_init_logger() -> None:
    """Test that logger initialization works correctly."""
    test_log_file: Final[str] = "test_logs.log"

    # Clear existing handlers
    logger = logging.getLogger()
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    init_logger(test_log_file)

    # Check that log file was created
    log_file = LOG_PATH / test_log_file
    assert log_file.exists()
    assert log_file.is_file()

    # Check that logger was configured correctly
    assert logger.level == logging.DEBUG
    assert len(logger.handlers) == 2

    # Clean up
    for handler in logger.handlers[:]:
        handler.close()
        logger.removeHandler(handler)
    log_file.unlink()


def test_log_config_info(valid_yaml_config_input: dict) -> None:
    """Test that config info logging works correctly.

    Args:
        valid_yaml_config_input: Fixture providing valid YAML config
    """
    # Initialize logger and config
    test_log_file: Final[str] = "test_logs.log"
    init_logger(test_log_file)
    config = YAMLConfig.parse_obj(valid_yaml_config_input)

    # Log config info
    log_config_info(config)

    # Check that log file contains expected info
    log_file = LOG_PATH / test_log_file
    log_contents = log_file.read_text()
    assert "Parsing config.yaml is complete" in log_contents
    assert "Proposer side name: men, Responder side name: women" in log_contents
    assert "Number of proposers: 4, Number of responders: 5" in log_contents
    assert "Preference type: random" in log_contents

    # Clean up
    log_file.unlink()


def test_timer_decorator() -> None:
    """Test that timer decorator works correctly."""
    # Initialize logger
    test_log_file: Final[str] = "test_logs.log"
    init_logger(test_log_file)

    # Define test function
    @timer_decorator
    def test_func() -> str:
        return "test"

    # Call function and check result
    result = test_func()
    assert result == "test"

    # Check that log file contains timing info
    log_file = LOG_PATH / test_log_file
    log_contents = log_file.read_text()
    assert "Method 'test_func' of module" in log_contents
    assert "executed in" in log_contents
    assert "seconds" in log_contents

    # Clean up
    log_file.unlink()
