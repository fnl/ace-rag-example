from fastapi import FastAPI
from pydantic import BaseModel

from ace_rag_example.services import LLMService, VectorStore


class QueryRequest(BaseModel):
    question: str
    top_k: int = 5


class SourceDocument(BaseModel):
    document_id: str


class QueryResponse(BaseModel):
    answer: str
    sources: list[SourceDocument]


def create_app(vector_store: VectorStore, llm_service: LLMService) -> FastAPI:
    app = FastAPI(title="ACE RAG Example")

    @app.post("/query", response_model=QueryResponse)
    def query(request: QueryRequest) -> QueryResponse:
        chunks = vector_store.search(request.question)
        chunks = chunks[: request.top_k]
        answer = llm_service.generate(request.question, chunks)
        sources = [SourceDocument(document_id=chunk["document_id"]) for chunk in chunks]
        return QueryResponse(answer=answer, sources=sources)

    return app
