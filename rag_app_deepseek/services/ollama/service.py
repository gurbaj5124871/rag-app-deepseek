from typing import Sequence

from ollama import AsyncClient, ChatResponse

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

    async def chat(self, user_prompt: str, system_prompt: str = "") -> ChatResponse:
        """
        Chat api.

        :param user_prompt: query prompt provided by end user
        :param system_prompt: admin prompt to keep llm guided

        :returns: ChatResponse
        """
        msgs = []

        if system_prompt:
            msgs.append({"role": "system", "content": user_prompt})

        msgs.append({"role": "user", "content": user_prompt})

        return await self.client.chat(
            model=self.model,
            messages=msgs,
        )
