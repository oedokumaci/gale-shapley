"""Exceptions for the project."""


class GSException(Exception):
    """Base exception class for the project."""


class ConfigError(GSException):
    """Exception class for errors in the config.yaml file."""


class TwoSidedMatchingError(ConfigError):
    """Exception class for when there are not exactly two sides to be matched."""

    def __init__(self, side_names: list[str]) -> None:
        self.message = f"Config input has {len(side_names)} sides to be matched. There should be exactly two"
        super().__init__(self.message)


class SideNameError(ConfigError):
    """Exception class for when a side name is not in SIDE_NAMES."""

    def __init__(self, side: str, side_names: list[str]) -> None:
        side_names_in_quotes = [f"'{g}'" for g in side_names]
        self.message = f'{side} should be {" or ".join(side_names_in_quotes)}'
        super().__init__(self.message)
