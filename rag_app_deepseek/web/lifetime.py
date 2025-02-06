import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI

from rag_app_deepseek.services.kafka.lifetime import init_kafka, shutdown_kafka
from rag_app_deepseek.services.milvus.lifetime import disconnect_milvus, init_milvus
from rag_app_deepseek.services.ollama.service import OllamaClient


@asynccontextmanager
async def lifespan(app: FastAPI):  # type: ignore
    """
    Actions to run on application startup and shutdown.

    This function uses fastAPI app to store data
    in the state, such as kafka consumer.

    :param app: the fastAPI application.
    """
    app.state.ollama_client = OllamaClient()
    await init_kafka(app)
    milvus_client = init_milvus()
    milvus_client.load_collection("text_embeddings_schema")
    app.state.milvus_client = milvus_client
    yield

    await shutdown_kafka(app)
    await asyncio.sleep(
        3,
    )  # sleep for 3 seconds so that milvus writes can be completed before disconnecting
    milvus_client.release_collection("text_embeddings_schema")
    disconnect_milvus(milvus_client)
