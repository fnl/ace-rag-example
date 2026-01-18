from typing import Any
from unittest.mock import Mock

import pytest


@pytest.fixture
def mock_vector_store() -> Mock:
    store = Mock()
    store.search.return_value = [
        {
            "document_id": "doc-001",
            "chunk_index": 0,
            "score": 0.92,
            "content": "The project overview describes the main goals.",
            "metadata": {"title": "Introduction", "author": "Jane Doe"},
        },
        {
            "document_id": "doc-001",
            "chunk_index": 1,
            "score": 0.87,
            "content": "The methodology section explains the approach.",
            "metadata": {"title": "Introduction", "author": "Jane Doe"},
        },
    ]
    return store


@pytest.fixture
def mock_llm_service() -> Mock:
    llm = Mock()
    llm.generate.return_value = (
        "The introduction covers the project overview and methodology."
    )
    return llm


@pytest.fixture
def client(mock_vector_store: Mock, mock_llm_service: Mock) -> Any:
    from fastapi.testclient import TestClient

    from ace_rag_example.api import create_app

    app = create_app(vector_store=mock_vector_store, llm_service=mock_llm_service)
    return TestClient(app)


def test_query_returns_answer_with_sources(
    client: Any, mock_vector_store: Mock, mock_llm_service: Mock
) -> None:
    response = client.post("/query", json={"question": "What topics are in the intro?"})

    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert (
        data["answer"]
        == "The introduction covers the project overview and methodology."
    )
    assert "sources" in data
    assert len(data["sources"]) == 2
    assert data["sources"][0]["document_id"] == "doc-001"
    assert data["sources"][0]["chunk_index"] == 0
    assert "score" in data["sources"][0]
    assert "content" in data["sources"][0]
