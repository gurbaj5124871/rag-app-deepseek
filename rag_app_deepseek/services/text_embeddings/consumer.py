import traceback
from dataclasses import dataclass
from datetime import datetime
from typing import List

from aiokafka import AIOKafkaConsumer
from fastapi import FastAPI
from loguru import logger
from pydantic import BaseModel
from pymilvus import MilvusClient

from rag_app_deepseek.services.ollama.service import OllamaClient
from rag_app_deepseek.services.text_embeddings.service import (
    InsertTextWithEmbeddingsIntoMilvusInput,
    insert_text_with_embeddings_into_milvus,
    split_text_into_chunks,
)


@dataclass
class KafkaMsgText(BaseModel):
    """KafkaMsgText dataclass to parse msg bytes in struct."""

    text: str
    timestamp: datetime


async def text_embeddings_consumer_handler(app: FastAPI) -> None:  # noqa: WPS210 WPS231
    """
    Handle kafka consumer messages.

    :param app: FastAPI object.
    :raises Exception: In case we fail generate embeddings or insert into milvus.
    :raises RuntimeError: If the data list is empty.
    """
    ollama_client: OllamaClient = app.state.ollama_client
    milvus_client: MilvusClient = app.state.milvus_client
    consumer: AIOKafkaConsumer = app.state.kafka_consumer_text_embeddings

    async for msg in consumer:
        try:
            logger.info(
                f"processing kafka consumer msg for topic: {msg.topic}, partition: {msg.partition}, offset: {msg.offset}",  # noqa: E501
            )
            msg_json = KafkaMsgText.model_validate_json(msg.value)
            chunks = split_text_into_chunks(msg_json.text)
            embeddings_res = await ollama_client.generate_embeddings_from_text(
                text=chunks,
            )

            text_with_embeddings: List[InsertTextWithEmbeddingsIntoMilvusInput] = []
            for i, chunk in enumerate(chunks):  # noqa: WPS111
                text_with_embeddings.append(
                    InsertTextWithEmbeddingsIntoMilvusInput(
                        text=chunk,
                        embedding=embeddings_res.embeddings[i],
                        timestamp_unix=int(msg_json.timestamp.timestamp()),
                    ),
                )
            insert_res = insert_text_with_embeddings_into_milvus(
                milvus_client=milvus_client,
                text_with_embeddings=text_with_embeddings,
            )
            if insert_res["insert_count"] != len(text_with_embeddings):
                raise RuntimeError(
                    "Database insertion failed: insert count does not match the input size.",  # noqa: E501
                )

            await consumer.commit()
            logger.info(
                f"processed kafka consumer msg for topic: {msg.topic}, partition: {msg.partition}, offset: {msg.offset}",  # noqa: E501
            )
        except Exception:
            logger.error(traceback.format_exc())
            raise  # to avoid losing the stack trace!
