"""This module parses and validates the config.yaml."""

from __future__ import annotations  # needed in 3.9 for | of Python 3.10

from pathlib import Path

import yaml
from pydantic import BaseModel, root_validator, validator
from pydantic.fields import ModelField

VALID_PREFERENCE_TYPES: tuple[str, ...] = ("random",)
PATH_TO_YAMLCONFIG: Path = Path(__file__).parents[2] / "config" / "config.yaml"


class YAMLConfig(BaseModel):
    """Parses and validates the config.yaml file. Inherits from pydantic BaseModel.

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

    @validator("proposer_side_name", "responder_side_name")
    def side_names_must_be_valid(cls, v: str, field: ModelField) -> str:
        if not v.isalpha():
            raise ValueError(
                f"{field.name} must be of letters, {v} is not a valid name"
            )
        return v

    @root_validator
    def side_names_must_be_different(
        cls, values: dict[str, str | int]
    ) -> dict[str, str | int]:
        if values["proposer_side_name"] == values["responder_side_name"]:
            raise ValueError(
                "proposer_side_name and responder_side_name must be different"
            )
        return values

    @validator("preference_type")
    def preference_type_must_be_valid(cls, v: str) -> str:
        if v not in VALID_PREFERENCE_TYPES:
            raise ValueError(
                f"preference_type should be {' or '.join(VALID_PREFERENCE_TYPES)}, {v} is not valid"
            )
        return v

    @validator("number_of_proposers", "number_of_responders")
    def number_of_each_side_member_must_be_positive(
        cls, v: int, field: ModelField
    ) -> int:
        if not v > 0:
            raise ValueError(f"{field.name} must be greater than 0, {v} is not")
        return v

    @validator("log_file_name")
    def log_file_name_must_be_valid(cls, v: str) -> str:
        if v.startswith("/"):
            raise ValueError(
                f"log_file_name should not start with /, {v} starts with /"
            )
        if not v.endswith(".log"):
            raise ValueError(f"log_file_name should be a .log file, {v} is not")
        # PROD CODE
        # log_file = Path(__file__).parents[2] / "logs" / v
        # if log_file.exists():  # if log file exists ask to overwrite
        #     user_input = input(f"log_file_name {v} already exists, overwrite? y/n (n)") or "n"
        #     if user_input != "y":
        #         raise SystemExit("exiting not to overwrite, please change log_file_name in config.yaml")
        return v


with PATH_TO_YAMLCONFIG.open() as yaml_config:
    config_input = YAMLConfig(**yaml.safe_load(yaml_config))
