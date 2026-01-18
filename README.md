# ace-rag-example

A RAG (Retrieval-Augmented Generation) web service that enables natural language queries against indexed document content.

## Overview

This service provides:

- **User API**: Natural language queries with AI-generated answers based on indexed content (implemented)
- **Admin API**: Bulk upsert and delete documents in the vector store (planned)

See [architecture.md](architecture.md) for sequence diagrams and REST API documentation.

## Tech Stack

**In Use:**

- **[FastAPI](https://fastapi.tiangolo.com/reference/)**: Web framework for the REST API

**Planned:**

- **[FAISS](https://github.com/facebookresearch/faiss/wiki)**: Persisted vector store for semantic similarity search
- **[BM25s](https://github.com/xhluca/bm25s)**: Transient full-text search using the BM25 algorithm
- **[LangFuse](https://langfuse.com/docs)**: Observability, tracing, and evaluation of the RAG pipeline

## Requirements

- Python 3.12+

## Development Setup

This project uses `uv` for package and environment management.

Install `uv` if not already available:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Clone the repository and set up the environment:

```bash
git clone https://github.com/fnl/ace-rag-example.git
cd ace-rag-example
uv venv
uv sync
```

Install the pre-commit hooks:

```bash
uvx pre-commit install
```

Dependencies are managed in `pyproject.toml`. To add new dependencies:

```bash
uv add <package>           # runtime dependency
uv add --dev <package>     # development dependency
```

## Pre-commit Hooks

The project uses pre-commit hooks to ensure code quality on every commit. The hooks run:

- **black**: Code formatting check
- **ruff**: Linting
- **ty**: Type checking
- **pytest**: Tests

To run all hooks manually:

```bash
uvx pre-commit run --all-files
```

## Testing

Run all tests:

```bash
uv run pytest tests
```

Run a specific test:

```bash
uv run pytest tests/test_query.py::test_query_returns_answer_with_sources -v
```

## Code Quality

Format code:

```bash
uv run black . tests
```

Lint and auto-fix:

```bash
uv run ruff check . tests --select E,F,W,S,B,C4,I,N --ignore E501 --fix
```

Type check:

```bash
uv run ty .
```

Audit dependencies:

```bash
uv run pip-audit
```

## Project Structure

```
ace-rag-example/
├── ace_rag_example/         # Application package
│   ├── api.py               # FastAPI application and endpoints
│   └── services.py          # Service protocol definitions
├── tests/                   # Test directory
│   └── test_query.py        # Query endpoint tests
├── architecture.md          # System architecture and API docs
├── pyproject.toml           # Project dependencies
├── .pre-commit-config.yaml  # Pre-commit hook configuration
└── README.md                # This file
```

## License

See LICENSE file for details.
