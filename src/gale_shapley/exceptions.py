"""Exceptions module."""


class GSException(Exception):
    """Base exception class for the project."""


class ConfigError(GSException):
    """Exception class for errors in the config.yaml file."""
