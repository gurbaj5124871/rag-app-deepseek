from typing import Any, AsyncGenerator
from unittest.mock import Mock

import pytest
from aiokafka import AIOKafkaProducer
from fastapi import FastAPI
from httpx import AsyncClient

from rag_app_deepseek.services.kafka.dependencies import get_kafka_producer
from rag_app_deepseek.services.kafka.lifetime import init_kafka, shutdown_kafka
from rag_app_deepseek.web.application import get_app


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    """
    Backend for anyio pytest plugin.

    :return: backend name.
    """
    return "asyncio"


@pytest.fixture
async def test_kafka_producer() -> AsyncGenerator[AIOKafkaProducer, None]:
    """
    Creates kafka's producer.

    :yields: kafka's producer.
    """
    app_mock = Mock()
    await init_kafka(app_mock)
    yield app_mock.state.kafka_producer
    await shutdown_kafka(app_mock)


@pytest.fixture
def fastapi_app(
    test_kafka_producer: AIOKafkaProducer,
) -> FastAPI:
    """
    Fixture for creating FastAPI app.

    :return: fastapi app with mocked dependencies.
    """
    application = get_app()
    application.dependency_overrides[get_kafka_producer] = lambda: test_kafka_producer
    return application  # noqa: WPS331


@pytest.fixture
async def client(
    fastapi_app: FastAPI,
    anyio_backend: Any,
) -> AsyncGenerator[AsyncClient, None]:
    """
    Fixture that creates client for requesting server.

    :param fastapi_app: the application.
    :yield: client for the app.
    """
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        yield ac
