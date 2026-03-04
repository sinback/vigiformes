# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**vigiformes** is a personal home-monitoring project targeting a Raspberry Pi 3A. The first product deliverable is a continuously-running audio pipeline that detects alarm calls from a pet bird (Kiwi). It is not a safety tool.

The project is not containerized — this is intentional, as containerization is impractical for a hardware project.

## Development Setup

Requires Python 3.14 via [pyenv](https://github.com/pyenv/pyenv). The `.python-version` file handles version selection automatically.

```bash
pyenv install 3.14
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
hooks/autohook.sh install
```

## Commands

```bash
ruff check .          # lint
ruff check --fix .    # lint + auto-fix
mypy .                # type checking
pytest                # run tests
```

## Architecture

- `recording/` — audio recording pipeline
  - `config.toml` — default configuration (ALSA device, sample duration, output directory, etc.)
  - `config.py` — Pydantic config parser; use `load_config(path)` to get a typed `Config` object
  - `samples/` — populated at runtime by the recording pipeline; not committed
- `hooks/` — git hooks via [Autohook](https://github.com/Autohook/Autohook); pre-commit runs ruff then mypy (stops on first failure), pre-push is encouragement
- `setup/` — shell scripts for bootstrapping a fresh Raspberry Pi environment
- `tests/` — pytest test suite

## Key Conventions

- **Validation**: use Pydantic `BaseModel` with `model_validate()` for all data/config parsing
- **Audio**: `sounddevice` is the chosen library for the recording pipeline (wraps PortAudio/ALSA); the working ALSA device is `hw:2,0`, format `S24_3LE`, 2 channels, 44100 Hz
- **Config files**: TOML preferred
- **Tests**: use fixtures and `tmp_path` for isolation; each test must clean up after itself so ordering never matters; every test function gets a given/when/then docstring
- **README**: when adding developer-facing utilities, consider whether the README needs updating or reorganization
