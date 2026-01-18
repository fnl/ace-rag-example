from unittest.mock import Mock

import pytest
from fastapi.testclient import TestClient

from ace_rag_example.api import create_app


@pytest.fixture
def mock_vector_store() -> Mock:
    store = Mock()
    store.search.return_value = [
        {"document_id": "doc-001", "chunk_index": 0, "score": 0.92, "content": "..."},
        {"document_id": "doc-002", "chunk_index": 0, "score": 0.87, "content": "..."},
    ]
    return store


@pytest.fixture
def mock_llm_service() -> Mock:
    llm = Mock()
    llm.generate.return_value = "Generated answer from LLM."
    return llm


@pytest.fixture
def client(mock_vector_store: Mock, mock_llm_service: Mock) -> TestClient:
    app = create_app(vector_store=mock_vector_store, llm_service=mock_llm_service)
    return TestClient(app)


def test_query_returns_answer_with_sources(client: TestClient) -> None:
    response = client.post("/query", json={"question": "What is the topic?"})

    data = response.json()
    assert "answer" in data
    assert "sources" in data
    source_ids = [s["document_id"] for s in data["sources"]]
    assert source_ids == ["doc-001", "doc-002"]


def test_query_with_top_k_uses_at_most_that_many_chunks(
    mock_llm_service: Mock,
) -> None:
    mock_vector_store = Mock()
    mock_vector_store.search.return_value = [
        {"document_id": f"doc-{i:03d}", "content": f"chunk {i}"} for i in range(10)
    ]
    app = create_app(vector_store=mock_vector_store, llm_service=mock_llm_service)
    client = TestClient(app)

    client.post("/query", json={"question": "What is the topic?", "top_k": 3})

    chunks_passed_to_llm = mock_llm_service.generate.call_args[0][1]
    assert len(chunks_passed_to_llm) <= 3
