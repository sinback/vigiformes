from pathlib import Path

import pytest
import tomllib
from pydantic import ValidationError

from recording.config import load_config

VALID_TOML_WRONG_TYPES = """
[output]
directory = "recording/samples"

[recording]
device = "hw:2,0"
duration_seconds = "five"   # "five" is valid TOML but Pydantic doesn't like it
channels = 2
sample_rate = 44100
format = "S24_3LE"
"""

VALID_TOML_UNSUPPORTED_FORMAT = """
[output]
directory = "recording/samples"

[recording]
device = "hw:2,0"
duration_seconds = 5
channels = 2
sample_rate = 44100
format = "MP3"  # that's a file format, not a recording format
"""


@pytest.fixture
def default_config_path() -> Path:
    return Path(__file__).parents[1] / "recording" / "config.toml"


def test_load_default_config(default_config_path: Path) -> None:
    """
    Given the default config.toml,
    when load_config is called,
    then it returns a Config with all fields matching the documented defaults.
    """
    config = load_config(default_config_path)

    assert config.output.directory == Path("recording/samples")
    assert config.recording.device == "hw:2,0"
    assert config.recording.duration_seconds == 5
    assert config.recording.channels == 2
    assert config.recording.sample_rate == 44100
    assert config.recording.format == "S24_3LE"


def test_missing_config_file(tmp_path: Path) -> None:
    """
    Given a path to a config file that does not exist,
    when load_config is called,
    then a FileNotFoundError is raised.
    """
    with pytest.raises(FileNotFoundError):
        load_config(tmp_path / "config.toml")


def test_unparseable_config_file(tmp_path: Path) -> None:
    """
    Given a config file containing invalid TOML,
    when load_config is called,
    then a TOMLDecodeError is raised.
    """
    bad_toml = tmp_path / "config.toml"
    bad_toml.write_text("this is not ] valid toml [")
    with pytest.raises(tomllib.TOMLDecodeError):
        load_config(bad_toml)


def test_invalid_config_values(tmp_path: Path) -> None:
    """
    Given a config file with valid TOML but wrong field types,
    when load_config is called,
    then a Pydantic ValidationError is raised.
    """
    bad_config = tmp_path / "config.toml"
    bad_config.write_text(VALID_TOML_WRONG_TYPES)
    with pytest.raises(ValidationError):
        load_config(bad_config)


def test_unsupported_format(tmp_path: Path) -> None:
    """
    Given a config file with a format value not in the supported AlsaFormat literals,
    when load_config is called,
    then a Pydantic ValidationError is raised.
    """
    bad_config = tmp_path / "config.toml"
    bad_config.write_text(VALID_TOML_UNSUPPORTED_FORMAT)
    with pytest.raises(ValidationError):
        load_config(bad_config)
