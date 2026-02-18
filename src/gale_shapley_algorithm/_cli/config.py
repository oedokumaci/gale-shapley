"""Config parser for the CLI. Parses and validates config.yaml."""

from pathlib import Path
from typing import Annotated, TypedDict

import yaml
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

VALID_PREFERENCE_TYPES: tuple[str, ...] = ("random", "input")
PATH_TO_YAMLCONFIG: Path = Path(__file__).parents[3] / "config" / "config.yaml"


class YAMLConfig(BaseModel):
    """Parses and validates the config.yaml file.

    Raises:
        ValueError
    """

    model_config = ConfigDict(validate_assignment=True)

    proposer_side_name: Annotated[str, Field(pattern=r"^[a-zA-Z]+$")]
    responder_side_name: Annotated[str, Field(pattern=r"^[a-zA-Z]+$")]
    preference_type: str
    number_of_proposers: Annotated[int, Field(gt=0)]
    number_of_responders: Annotated[int, Field(gt=0)]
    log_file_name: str
    proposers: dict[str, list[str]] = Field(default_factory=dict)
    responders: dict[str, list[str]] = Field(default_factory=dict)

    @model_validator(mode="before")
    @classmethod
    def side_names_must_be_different(cls, data: dict) -> dict:
        """Validate that side names are different (case-insensitive)."""
        if str(data.get("proposer_side_name", "")).casefold() == str(data.get("responder_side_name", "")).casefold():
            raise ValueError("'proposer_side_name' and 'responder_side_name' must be different, case insensitive")
        return data

    @field_validator("preference_type")
    @classmethod
    def preference_type_must_be_valid(cls, v: str) -> str:
        """Validate that preference type is valid."""
        if v.casefold() not in VALID_PREFERENCE_TYPES:
            raise ValueError(
                f"'preference_type' should be {' or '.join(VALID_PREFERENCE_TYPES)} case insensitive, {v!r} is not valid"
            )
        return v

    @field_validator("log_file_name")
    @classmethod
    def log_file_name_must_be_valid(cls, v: str) -> str:
        """Validate that log file name is valid."""
        if v.startswith("/"):
            raise ValueError(f"log_file_name should not start with /, {v!r} starts with /")
        if not v.endswith(".log"):
            raise ValueError(f"log_file_name should be a .log file, {v!r} is not")
        return v

    @model_validator(mode="after")
    def input_must_be_valid(self) -> "YAMLConfig":
        """Validate input preferences if preference_type is 'input'."""
        if self.preference_type.casefold() == "input":
            for side in ("proposers", "responders"):
                other_side = "responders" if side == "proposers" else "proposers"
                side_dict = getattr(self, side)
                other_side_dict = getattr(self, other_side)

                for person, preferences in side_dict.items():
                    for preference in preferences:
                        if preference not in other_side_dict:
                            raise ValueError(f"Preference {preference!r} of person {person!r} is not in {side!r}")
                if not side_dict:
                    raise ValueError(f"no {side!r} inputted")
                if len(side_dict) != getattr(self, f"number_of_{side}"):
                    import warnings

                    warnings.warn(
                        f"number of {side!r} inputted does not match 'number_of_{side}' in 'config.yaml'",
                        stacklevel=2,
                    )
        return self


class YAMLConfigDict(TypedDict):
    """Type hints for YAML configuration dictionary."""

    proposer_side_name: str
    responder_side_name: str
    preference_type: str
    number_of_proposers: int
    number_of_responders: int
    log_file_name: str
    proposers: dict[str, list[str]]
    responders: dict[str, list[str]]


def side_swap(config_input: YAMLConfig) -> None:
    """Swap proposer and responder sides.

    Args:
        config_input: config input to swap sides
    """
    swapped_data = {
        "proposer_side_name": config_input.responder_side_name,
        "responder_side_name": config_input.proposer_side_name,
        "number_of_proposers": config_input.number_of_responders,
        "number_of_responders": config_input.number_of_proposers,
        "proposers": config_input.responders,
        "responders": config_input.proposers,
        "preference_type": config_input.preference_type,
        "log_file_name": config_input.log_file_name,
    }

    new_config = YAMLConfig.model_validate(swapped_data)

    for key, value in new_config.model_dump().items():
        object.__setattr__(config_input, key, value)


def load_config() -> YAMLConfig:
    """Load and parse config.yaml.

    Returns:
        Parsed and validated YAMLConfig.

    Raises:
        FileNotFoundError: If config.yaml does not exist.
    """
    with PATH_TO_YAMLCONFIG.open(encoding="utf-8") as yaml_config:
        config_data = yaml.safe_load(yaml_config)
    config_data = {k.casefold(): v for k, v in config_data.items()}
    return YAMLConfig.model_validate(config_data)
