import traceback
from dataclasses import dataclass
from datetime import datetime

from aiokafka import AIOKafkaConsumer
from loguru import logger
from pydantic import BaseModel

from rag_app_deepseek.services.ollama.ollama_services import OllamaClient


@dataclass
class KafkaMsgText(BaseModel):
    """KafkaMsgText dataclass to parse msg bytes in struct."""

    text: str
    timestamp: datetime


async def text_embeddings_consumer_handler(consumer: AIOKafkaConsumer) -> None:
    """
    Handle kafka consumer messages.

    :param consumer: kafka consumer for text embeddings.
    :raises Exception: In case we fail to log.
    """
    ollama_client = OllamaClient()

    async for msg in consumer:
        try:
            msg_json = KafkaMsgText.model_validate_json(msg.value)

            text_embeddings = await ollama_client.generate_embeddings_from_text(
                msg_json.text,
            )
            logger.info(f"text embeddings generated: {text_embeddings}")

            await consumer.commit()
        except Exception:
            logger.error(traceback.format_exc())
            raise  # to avoid losing the stack trace!
