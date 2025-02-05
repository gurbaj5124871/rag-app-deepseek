from loguru import logger
from pymilvus import connections

from rag_app_deepseek.settings import settings


def init_milvus() -> None:
    """
    Initialises Milvus (Vector Store DB) connection.

    The library ensures that multiple connections
    are not created by having connections as a Singleton.
    """
    connections.connect(
        alias=settings.milvus_conn_name,
        host=settings.milvus_host,
        port=settings.milvus_port,
        user=settings.milvus_username,
        password=settings.milvus_password,
        keep_alive=True,
    )
    logger.info("milvus db connected")


def disconnect_milvus() -> None:
    """Disconnects the db connection."""
    connections.disconnect(settings.milvus_conn_name)
    logger.info("milvus db disconnected")
