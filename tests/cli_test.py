"""Tests for the CLI module."""

import typer
from typer.testing import CliRunner

from gale_shapley_algorithm._cli.app import main

app = typer.Typer()
app.command()(main)
runner = CliRunner()


def test_cli_no_existing_log(tmp_path, monkeypatch):
    """Test CLI when no log file exists."""
    monkeypatch.setattr("gale_shapley_algorithm._cli.app.LOG_PATH", tmp_path)
    result = runner.invoke(app, ["1", "--no-print-all-preferences", "--no-report-matches"])
    assert result.exit_code == 0


def test_cli_existing_log_overwrite_yes(tmp_path, monkeypatch):
    """Test CLI with existing log file and user says 'y'."""
    monkeypatch.setattr("gale_shapley_algorithm._cli.app.LOG_PATH", tmp_path)
    from gale_shapley_algorithm._cli.config import load_config

    config = load_config()
    log_file = tmp_path / config.log_file_name
    log_file.touch()
    monkeypatch.setattr("builtins.input", lambda _: "y")
    result = runner.invoke(app, ["1", "--no-print-all-preferences", "--no-report-matches"])
    assert result.exit_code == 0


def test_cli_existing_log_overwrite_no(tmp_path, monkeypatch):
    """Test CLI with existing log file and user says 'n'."""
    monkeypatch.setattr("gale_shapley_algorithm._cli.app.LOG_PATH", tmp_path)
    from gale_shapley_algorithm._cli.config import load_config

    config = load_config()
    log_file = tmp_path / config.log_file_name
    log_file.touch()
    monkeypatch.setattr("builtins.input", lambda _: "n")
    result = runner.invoke(app, ["1"])
    assert result.exit_code == 1


def test_cli_existing_log_default_enter(tmp_path, monkeypatch):
    """Test CLI with existing log file and user presses Enter (default 'n')."""
    monkeypatch.setattr("gale_shapley_algorithm._cli.app.LOG_PATH", tmp_path)
    from gale_shapley_algorithm._cli.config import load_config

    config = load_config()
    log_file = tmp_path / config.log_file_name
    log_file.touch()
    monkeypatch.setattr("builtins.input", lambda _: "")
    result = runner.invoke(app, ["1"])
    assert result.exit_code == 1


def test_cli_swap_sides(tmp_path, monkeypatch):
    """Test CLI with --swap-sides flag."""
    monkeypatch.setattr("gale_shapley_algorithm._cli.app.LOG_PATH", tmp_path)
    result = runner.invoke(app, ["1", "--swap-sides", "--no-print-all-preferences", "--no-report-matches"])
    assert result.exit_code == 0


def test_cli_all_options_disabled(tmp_path, monkeypatch):
    """Test CLI with all display options disabled."""
    monkeypatch.setattr("gale_shapley_algorithm._cli.app.LOG_PATH", tmp_path)
    result = runner.invoke(
        app,
        ["1", "--no-print-all-preferences", "--no-compact", "--no-report-matches"],
    )
    assert result.exit_code == 0
