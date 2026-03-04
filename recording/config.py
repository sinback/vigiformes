from pathlib import Path

import tomllib
from pydantic import BaseModel


class OutputConfig(BaseModel):
    directory: Path


class RecordingConfig(BaseModel):
    device: str
    duration_seconds: int
    channels: int
    sample_rate: int
    format: str


class Config(BaseModel):
    output: OutputConfig
    recording: RecordingConfig


def load_config(path: Path) -> Config:
    with open(path, "rb") as f:
        raw = tomllib.load(f)
    return Config.model_validate(raw)
