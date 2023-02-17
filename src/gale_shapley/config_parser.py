"""This module parses and validates the config.yaml.
If the config.yaml is valid, logger is initialized here."""

import logging
import os

import yaml
from pydantic import BaseModel, validator
from pydantic.fields import ModelField

from gale_shapley.exceptions import ConfigError
from gale_shapley.utils import init_logger

PREFERENCE_TYPES: tuple[str] = ("random",)
PATH_TO_YAMLCONFIG: str = (
    os.path.dirname(__file__).split("src")[0] + "config/config.yaml"
)


class YAMLConfig(BaseModel):
    """Parses and validates the config.yaml file. Inherits from pydantic BaseModel.
    One can use @dataclass decorator instead of BaseModel, but validation is not as easy as with BaseModel.

    Raises:
        ConfigError
    """

    proposer_side_name: str
    responder_side_name: str
    preference_type: str
    number_of_proposers: int
    number_of_responders: int
    log_file_name: str

    @validator("preference_type")
    def preference_type_must_be_valid(cls, v: str) -> str:
        if v not in PREFERENCE_TYPES:
            raise ConfigError(
                f"preference_type should be {' or '.join(PREFERENCE_TYPES)}, {v} is not valid"
            )
        return v

    @validator("number_of_proposers", "number_of_responders")
    def number_of_each_side_member_must_be_positive(
        cls, v: int, field: ModelField
    ) -> int:
        if not v > 0:
            raise ConfigError(f"{field.name} must be greater than 0, {v} is not")
        return v

    @validator("log_file_name")
    def log_file_name_must_be_valid(cls, v: str) -> str:
        if v.startswith("/"):
            raise ConfigError(
                f"log_file_name should not start with /, {v} starts with /"
            )
        if not v.endswith(".log"):
            raise ConfigError(f"log_file_name should be a .log file, {v} is not")
        # PROD CODE
        # if os.path.exists(f"../../logs/{v}"):  # if log file exists ask to overwrite
        #     user_input = input(f"log_file_name {v} already exists, overwrite? y/n (n)") or "n"
        #     if user_input != "y":
        #         raise SystemExit("exiting not to overwrite, please change log_file_name in config.yaml")
        return v


with open(PATH_TO_YAMLCONFIG) as yaml_config:
    config_input = YAMLConfig(**yaml.safe_load(yaml_config))

init_logger(config_input.log_file_name)
logging.info("Parsing config.yaml is complete")
logging.info(
    f"Proposer side name: {config_input.proposer_side_name}, Responder side name: {config_input.responder_side_name}"
)
logging.info(
    f"Number of proposers: {config_input.number_of_proposers}, Number of responders: {config_input.number_of_responders}"
)
logging.info(f"Preference type: {config_input.preference_type}")
