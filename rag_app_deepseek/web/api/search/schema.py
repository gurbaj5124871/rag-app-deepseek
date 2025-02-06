from pydantic import BaseModel


class PromptSemanticSearch(BaseModel):
    """Prompt LLM with query."""

    query: str
