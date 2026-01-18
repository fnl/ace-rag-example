from typing import Any, Protocol


class VectorStore(Protocol):
    def search(self, query: str, top_k: int = 5) -> list[dict[str, Any]]:
        """Search for similar documents in the vector store."""
        ...


class LLMService(Protocol):
    def generate(self, prompt: str, context: list[dict[str, Any]]) -> str:
        """Generate a response using the LLM with the given context."""
        ...
