from __future__ import annotations
import json
from pathlib import Path
from pydantic import BaseModel
from typing import Literal


class ProviderConfig(BaseModel):
    name: Literal["openai", "google"]
    model: str
    api_key: str


class AIConfig(BaseModel):
    providers: list[ProviderConfig]


class Dataset(BaseModel):
    dir_path: Path
    instruction_file: Path
    prompt_file: Path
    output_dir: Path
    response_file: Path
    repetitions: int


class Config(BaseModel):
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    dataset: Dataset
    ai: AIConfig

    @classmethod
    def from_json_file(cls, config_path: str | Path) -> Config:
        try:
            with open(config_path, "r", encoding="utf-8") as file:
                config_data = json.load(file)

            return cls.model_validate(config_data)

        except Exception as error:
            raise RuntimeError(
                f"Failed to load config from '{config_path}': {error}")
