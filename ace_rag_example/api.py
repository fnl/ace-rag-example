from typing import Any

from fastapi import FastAPI
from pydantic import BaseModel

from ace_rag_example.services import LLMService, VectorStore


class QueryRequest(BaseModel):
    question: str


class SourceDocument(BaseModel):
    document_id: str
    chunk_index: int
    score: float
    content: str
    metadata: dict[str, Any] | None = None


class QueryResponse(BaseModel):
    answer: str
    sources: list[SourceDocument]


def create_app(vector_store: VectorStore, llm_service: LLMService) -> FastAPI:
    app = FastAPI(title="ACE RAG Example")

    @app.post("/query", response_model=QueryResponse)
    def query(request: QueryRequest) -> QueryResponse:
        chunks = vector_store.search(request.question)
        answer = llm_service.generate(request.question, chunks)
        sources = [
            SourceDocument(
                document_id=chunk["document_id"],
                chunk_index=chunk["chunk_index"],
                score=chunk["score"],
                content=chunk["content"],
                metadata=chunk.get("metadata"),
            )
            for chunk in chunks
        ]
        return QueryResponse(answer=answer, sources=sources)

    return app
