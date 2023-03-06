"""This module parses and validates the config.yaml."""

from __future__ import annotations  # needed in 3.9 for | of Python 3.10

import warnings
from pathlib import Path

import yaml
from pydantic import BaseModel, root_validator, validator
from pydantic.fields import ModelField

VALID_PREFERENCE_TYPES: tuple[str, ...] = ("random", "input")
PATH_TO_YAMLCONFIG: Path = Path(__file__).parents[2] / "config" / "config.yaml"


class YAMLConfig(BaseModel):
    """Parses and validates the config.yaml file.
    Inherits from pydantic BaseModel.

    Raises:
        ValueError
    """

    # One can use also use pydantic's @dataclass decorator instead of BaseModel, which accepts validators.
    # See https://github.com/pydantic/pydantic/issues/710 for a discussion.

    proposer_side_name: str
    responder_side_name: str
    preference_type: str
    number_of_proposers: int
    number_of_responders: int
    log_file_name: str
    proposers: dict[
        str, list[str]
    ] = {}  # mutable default values are fine, pydantic takes care of it
    responders: dict[str, list[str]] = {}

    @validator("proposer_side_name", "responder_side_name")
    def side_names_must_be_valid(cls, v: str, field: ModelField) -> str:
        if not v.isalpha():
            raise ValueError(
                f"{field.name} must be of letters, {v} is not a valid name"
            )
        return v

    @root_validator
    def side_names_must_be_different(
        cls, values: dict[str, str | int | dict[str, list[str]]]
    ) -> dict[str, str | int | dict[str, list[str]]]:
        if (
            str(values["proposer_side_name"]).casefold()  # type: ignore
            == str(values["responder_side_name"]).casefold()  # type: ignore
            # for why casefold but not lower see https://docs.python.org/3/library/stdtypes.html
        ):
            raise ValueError(
                "'proposer_side_name' and 'responder_side_name' must be different, case insensitive"
            )
        return values

    @validator("preference_type")
    def preference_type_must_be_valid(cls, v: str) -> str:
        if v.casefold() not in VALID_PREFERENCE_TYPES:
            raise ValueError(
                f"'preference_type' should be {' or '.join(VALID_PREFERENCE_TYPES)} case insensitive, {v} is not valid"
            )
        return v

    @validator("number_of_proposers", "number_of_responders")
    def number_of_each_side_person_must_be_positive(
        cls, v: int, field: ModelField
    ) -> int:
        if not v > 0:
            raise ValueError(f"{field.name!r} must be greater than 0, {v!r} is not")
        return v

    @validator("log_file_name")
    def log_file_name_must_be_valid(cls, v: str) -> str:
        if v.startswith("/"):
            raise ValueError(
                f"log_file_name should not start with /, {v!r} starts with /"
            )
        if not v.endswith(".log"):
            raise ValueError(f"log_file_name should be a .log file, {v!r} is not")
        # PROD CODE
        # log_file = Path(__file__).parents[2] / "logs" / v
        # if log_file.exists():  # if log file exists ask to overwrite
        #     user_input = input(f"log_file_name {v} already exists, overwrite? y/n (n)") or "n"
        #     if user_input != "y":
        #         raise SystemExit("exiting not to overwrite, please change 'log_file_name' in 'config.yaml'")
        return v

    @root_validator
    def input_must_be_valid(
        cls, values: dict[str, str | int | dict[str, list[str]]]
    ) -> dict[str, str | int | dict[str, list[str]]]:
        if values["preference_type"].casefold() == "input":  # type: ignore
            for side in ("proposers", "responders"):
                other_side = "responders" if side == "proposers" else "proposers"
                for person, preferences in values[side].items():  # type: ignore
                    for preference in preferences:
                        if preference not in values[other_side]:  # type: ignore
                            raise ValueError(
                                f"Preference {preference!r} of person {person!r} is not in {side!r}"
                            )
                if len(values[side]) == 0:  # type: ignore
                    raise ValueError(f"no {side!r} inputted")
                elif len(values[side]) != values[f"number_of_{side}"]:  # type: ignore
                    warnings.warn(
                        f"number of {side!r} inputted does not match 'number_of_{side}' in 'config.yaml'",
                        stacklevel=2,
                    )
        return values


with PATH_TO_YAMLCONFIG.open() as yaml_config:
    config_data = yaml.safe_load(yaml_config)
config_data = {k.casefold(): v for k, v in config_data.items()}
config_input = YAMLConfig(**config_data)
