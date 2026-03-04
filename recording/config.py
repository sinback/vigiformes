from pathlib import Path
from typing import Literal

import tomllib
from pydantic import BaseModel

AlsaFormat = Literal["S16_LE", "S24_3LE", "S32_LE"]


class OutputConfig(BaseModel):
    directory: Path


class RecordingConfig(BaseModel):
    device: str
    duration_seconds: int
    channels: int
    sample_rate: int
    format: AlsaFormat


class Config(BaseModel):
    output: OutputConfig
    recording: RecordingConfig


def load_config(path: Path) -> Config:
    with open(path, "rb") as f:
        raw = tomllib.load(f)
    return Config.model_validate(raw)
