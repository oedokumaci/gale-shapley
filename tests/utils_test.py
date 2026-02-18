"""Tests for the CLI logging/utils module."""

from pathlib import Path
from typing import Final
from unittest.mock import patch

from gale_shapley._cli.config import YAMLConfig
from gale_shapley._cli.logging import init_logger, log_config_info, timer_decorator


def test_init_logger(tmp_path: Path) -> None:
    with patch("gale_shapley._cli.logging.LOG_PATH", tmp_path):
        init_logger("test.log")

    import logging

    from rich.logging import RichHandler

    logger = logging.getLogger()
    assert logger.level == logging.DEBUG
    handler_types = [type(h) for h in logger.handlers]
    assert logging.FileHandler in handler_types
    assert RichHandler in handler_types
    assert (tmp_path / "test.log").exists()


def test_log_config_info_random(tmp_path: Path, valid_yaml_config_input: dict) -> None:
    with patch("gale_shapley._cli.logging.LOG_PATH", tmp_path):
        init_logger("test.log")

    config = YAMLConfig.model_validate(valid_yaml_config_input)
    log_config_info(config)

    log_contents: Final[str] = (tmp_path / "test.log").read_text(encoding="utf-8")
    assert "Parsing config.yaml is complete" in log_contents
    assert "Proposer side name: men" in log_contents
    assert "Number of proposers: 4" in log_contents
    assert "Preference type: random" in log_contents


def test_log_config_info_input(tmp_path: Path, valid_input_yaml_config: dict) -> None:
    """Test log_config_info with preference_type='input'."""
    with patch("gale_shapley._cli.logging.LOG_PATH", tmp_path):
        init_logger("test.log")

    config = YAMLConfig.model_validate(valid_input_yaml_config)
    log_config_info(config)

    log_contents: Final[str] = (tmp_path / "test.log").read_text(encoding="utf-8")
    assert "Parsing config.yaml is complete" in log_contents
    assert "Number of proposers: 2" in log_contents
    assert "Preference type: input" in log_contents


def test_timer_decorator(tmp_path: Path) -> None:
    with patch("gale_shapley._cli.logging.LOG_PATH", tmp_path):
        init_logger("test.log")

    @timer_decorator
    def test_func() -> str:
        return "test"

    result = test_func()
    assert result == "test"

    log_contents: Final[str] = (tmp_path / "test.log").read_text(encoding="utf-8")
    assert "Method 'test_func'" in log_contents
    assert "executed in" in log_contents
