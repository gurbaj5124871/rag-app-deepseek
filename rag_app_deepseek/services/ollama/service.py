from typing import Sequence

from ollama import AsyncClient

from rag_app_deepseek.settings import settings


class OllamaClient:
    """
    Ollama client.

    It interacts with the model's apis
    """

    client = AsyncClient(host=settings.ollama_host)
    model = settings.ollama_model

    async def generate_embeddings_from_text(self, text: Sequence[str]):  # type: ignore
        """
        Generates embeddings from the text provided.

        :param text: string to generate embeddings for
        :returns: text embeddings result
        """
        return await self.client.embed(model=self.model, input=text)
