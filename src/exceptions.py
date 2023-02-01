"""Exceptions for the project."""


class GSException(Exception):
    """Base exception class for the project."""


class ConfigError(GSException):
    """Exception class for errors in the config.yaml file."""


class TwoSidedMatchingError(ConfigError):
    """Exception class for when there are not exactly two sides to be matched."""

    def __init__(self, side_names: list[str]) -> None:
        self.message = f"Config.yaml has {len(side_names)} side(s) to be matched. There should be exactly two"
        super().__init__(self.message)
