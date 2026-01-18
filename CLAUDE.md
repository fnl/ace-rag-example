# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

ace-rag-example is a Python application using uv for package management. Python 3.12+ required.

## Development Commands

All commands must be run via `uv run`:

```bash
uv run black . tests          # Format code
uv run ruff check . tests --select E,F,W,S,B,C4,I,N --ignore E501 --fix  # Lint
uv run ty .                   # Type check
uv run pytest tests           # Run all tests
uv run pytest tests/test_foo.py::test_specific -v  # Run single test
uv run pip-audit              # Audit dependencies
```

Install dev dependencies:

```bash
uv add --dev black ruff ty pytest pip-audit
```

## Code Structure

- `main.py` - Application entry point
- `tests/` - Test directory (to be created)
