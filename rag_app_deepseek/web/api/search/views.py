from fastapi import APIRouter, FastAPI, Query, Request
from pymilvus import MilvusClient

from rag_app_deepseek.services.ollama.service import OllamaClient
from rag_app_deepseek.services.text_embeddings.service import (
    get_texts_matching_vector_search,
)

router = APIRouter()


@router.get("/")
async def send_echo_message(  # noqa: WPS210
    request: Request,
    query: str = Query(
        ...,
        max_length=250,  # noqa: WPS432
        description="user query which user wants to get answered for",
    ),
) -> str:
    """
    Answers to users query by retrieving context data and passing it along to llm.

    :param request: fastapi app instance
    :param query: incoming query to prompt the llm.
    :returns: returns the result.
    """
    app: FastAPI = request.app
    ollama_client: OllamaClient = app.state.ollama_client
    milvus_client: MilvusClient = app.state.milvus_client

    ctx_embeddings_res = await ollama_client.generate_embeddings_from_text([query])
    ctx_embedding = ctx_embeddings_res.embeddings[0]

    ctx_texts = get_texts_matching_vector_search(
        milvus_client=milvus_client,
        embedding_to_match=ctx_embedding,
    )
    ctx_texts_filtered = list(  # noqa: F841
        filter(lambda data: data["distance"] > 0.47, ctx_texts),  # noqa: WPS459 WPS432
    )

    return "wip"
