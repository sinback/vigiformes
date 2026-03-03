# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**vigiformes** is a personal home-monitoring toy (not a safety tool). The project is Python-based and likely involves audio processing given the presence of `test.wav`.

## Setup

No build system is configured yet. When Python dependencies are added, expect tooling from the `.gitignore` patterns: Poetry, PDM, Pixi, or UV as package managers; pytest for testing; Ruff for linting.

## Notes

- This is a personal/experimental project, not production software
- The `.gitignore` is configured for Python development with common IDE and virtualenv exclusions
