"""This module parses and validates the config.yaml."""

import os

import yaml
from pydantic import BaseModel, validator
from pydantic.fields import ModelField

VALID_PREFERENCE_TYPES: tuple[str] = ("random",)
PATH_TO_YAMLCONFIG: str = (
    os.path.dirname(__file__).split("src")[0] + "config/config.yaml"
)


class YAMLConfig(BaseModel):
    """Parses and validates the config.yaml file. Inherits from pydantic BaseModel.
    One can use @dataclass decorator instead of BaseModel, but validation is not as easy as with BaseModel.

    Raises:
        ValueError
    """

    proposer_side_name: str
    responder_side_name: str
    preference_type: str
    number_of_proposers: int
    number_of_responders: int
    log_file_name: str

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
        # if os.path.exists(f"../../logs/{v}"):  # if log file exists ask to overwrite
        #     user_input = input(f"log_file_name {v} already exists, overwrite? y/n (n)") or "n"
        #     if user_input != "y":
        #         raise SystemExit("exiting not to overwrite, please change log_file_name in config.yaml")
        return v


with open(PATH_TO_YAMLCONFIG) as yaml_config:
    config_input = YAMLConfig(**yaml.safe_load(yaml_config))
