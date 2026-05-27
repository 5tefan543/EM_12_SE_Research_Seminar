from __future__ import annotations
import json
from pathlib import Path
from pydantic import BaseModel


class OpenAICredentials(BaseModel):
    api_key: str


class GoogleCredentials(BaseModel):
    api_key: str


class Credentials(BaseModel):
    openai: OpenAICredentials
    google: GoogleCredentials

class Dataset(BaseModel):
    dir_path: Path
    instruction_file: Path
    prompt_file: Path
    response_file: Path
    repetitions: int


class Config(BaseModel):
    dataset: Dataset
    credentials: Credentials

    @classmethod
    def from_json_file(cls, config_path: str | Path) -> Config:
        try:
            with open(config_path, "r", encoding="utf-8") as file:
                config_data = json.load(file)

            return cls.model_validate(config_data)

        except Exception as error:
            raise RuntimeError(
                f"Failed to load config from '{config_path}': {error}")
