"""Exceptions for the project."""
from typing import List  # need for Python<3.9


class GSException(Exception):
    """Base exception for the project."""

    pass


class ConfigError(GSException):
    pass


class TwoSidedMatchingError(GSException):
    def __init__(self, side_names: List[str]) -> None:
        self.message = f"There are {len(side_names)} sides to be matched. There should be exactly two"
        super().__init__(self.message)


class SideNameError(GSException):
    def __init__(self, side: str, side_names: List[str]) -> None:
        side_names_in_quotes = [f"'{g}'" for g in side_names]
        self.message = f'{side} should be {" or ".join(side_names_in_quotes)}'
        super().__init__(self.message)
