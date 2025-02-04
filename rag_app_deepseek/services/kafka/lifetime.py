import asyncio
import ssl

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from fastapi import FastAPI
from loguru import logger

from rag_app_deepseek.services.text_embeddings.text_embeddings_consumer import (
    text_embeddings_consumer_handler,
)
from rag_app_deepseek.settings import settings


async def init_kafka(app: FastAPI) -> None:  # pragma: no cover
    """
    Initialize kafka producer needed for test cases and consumer for text embeddings.

    This function creates producer
    and makes initial connection to
    the kafka cluster. After that you
    can use producer stored in state.

    We don't need to use pools here,
    because aiokafka has implicit pool
    inside the producer.

    :param app: current application.
    """
    if settings.kafka_ssl and settings.kafka_sasl_mechanism in [  # noqa: WPS337 WPS510
        "SCRAM-SHA-256",
        "SCRAM-SHA-512",
    ]:
        security_protocol = "SASL_SSL"
    elif settings.kafka_ssl:
        security_protocol = "SSL"
    else:
        security_protocol = "PLAINTEXT"

    use_sasl = (
        settings.kafka_sasl_mechanism
        and settings.kafka_sasl_username
        and settings.kafka_sasl_password
    ) is not None

    # Define SSL context
    context = ssl.create_default_context()
    context.options &= ssl.OP_NO_TLSv1
    context.options &= ssl.OP_NO_TLSv1_1

    kafka_common_config = {
        "bootstrap_servers": settings.kafka_bootstrap_servers_list,
        "security_protocol": security_protocol,
        "sasl_mechanism": settings.kafka_sasl_mechanism if use_sasl else "PLAIN",
        "ssl_context": context if settings.kafka_ssl else None,
        "sasl_plain_username": settings.kafka_sasl_username,
        "sasl_plain_password": settings.kafka_sasl_password,
    }

    app.state.kafka_producer = AIOKafkaProducer(**kafka_common_config)
    await app.state.kafka_producer.start()
    logger.info("Kafka producer started")

    app.state.kafka_consumer_text_embeddings = AIOKafkaConsumer(
        settings.kafka_topic_text,
        **kafka_common_config,
        client_id=f"rag-app-consumer-{settings.environment}",
        group_id=f"rag-app-consumer-{settings.environment}",
        auto_offset_reset="earliest",
        enable_auto_commit=False,
        max_poll_interval_ms=60000,  # 1 minute # noqa: WPS432
        session_timeout_ms=120000,  # 2 minutes # noqa: WPS432
    )
    await app.state.kafka_consumer_text_embeddings.start()

    app.state.kafka_consumer_text_embeddings_task = asyncio.create_task(
        kafka_consumer_handler(app),
    )
    logger.info("Kafka consumer started")


async def kafka_consumer_handler(app: FastAPI) -> None:
    """
    Handle kafka consumer messages.

    :param app: current application.
    """
    await text_embeddings_consumer_handler(
        app.state.kafka_consumer_text_embeddings,
    )


async def shutdown_kafka(app: FastAPI) -> None:  # pragma: no cover
    """
    Shutdown kafka client.

    This function closes all connections
    and sends all pending data to kafka.
    will leave consumer group; perform autocommit if enabled.

    :param app: current application.
    """
    app.state.kafka_consumer_text_embeddings_task.cancel()
    await app.state.kafka_consumer_text_embeddings.stop()
    await app.state.kafka_producer.stop()
