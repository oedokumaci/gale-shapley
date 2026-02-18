"""Tests for the CLI logging/utils module."""

import logging
from typing import Final

from gale_shapley._cli.config import YAMLConfig
from gale_shapley._cli.logging import LOG_PATH, init_logger, log_config_info, timer_decorator


def test_init_logger() -> None:
    test_log_file: Final[str] = "test_logs.log"
    logger = logging.getLogger()
    logger.handlers.clear()

    init_logger(test_log_file)

    log_file = LOG_PATH / test_log_file
    assert log_file.exists()
    assert logger.level == logging.DEBUG
    assert len(logger.handlers) == 2

    for handler in logger.handlers[:]:
        handler.close()
        logger.removeHandler(handler)
    log_file.unlink()


def test_log_config_info_random(valid_yaml_config_input: dict) -> None:
    test_log_file: Final[str] = "test_logs.log"
    init_logger(test_log_file)
    config = YAMLConfig.model_validate(valid_yaml_config_input)

    log_config_info(config)

    log_file = LOG_PATH / test_log_file
    log_contents = log_file.read_text(encoding="utf-8")
    assert "Parsing config.yaml is complete" in log_contents
    assert "Proposer side name: men" in log_contents
    assert "Number of proposers: 4" in log_contents
    assert "Preference type: random" in log_contents

    log_file.unlink()


def test_log_config_info_input(valid_input_yaml_config: dict) -> None:
    """Test log_config_info with preference_type='input'."""
    test_log_file: Final[str] = "test_logs_input.log"
    init_logger(test_log_file)
    config = YAMLConfig.model_validate(valid_input_yaml_config)

    log_config_info(config)

    log_file = LOG_PATH / test_log_file
    log_contents = log_file.read_text(encoding="utf-8")
    assert "Parsing config.yaml is complete" in log_contents
    assert "Number of proposers: 2" in log_contents
    assert "Preference type: input" in log_contents

    log_file.unlink()


def test_timer_decorator() -> None:
    test_log_file: Final[str] = "test_logs.log"
    init_logger(test_log_file)

    @timer_decorator
    def test_func() -> str:
        return "test"

    result = test_func()
    assert result == "test"

    log_file = LOG_PATH / test_log_file
    log_contents = log_file.read_text(encoding="utf-8")
    assert "Method 'test_func'" in log_contents
    assert "executed in" in log_contents

    log_file.unlink()
