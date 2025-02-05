from loguru import logger
from pymilvus import MilvusClient

from rag_app_deepseek.settings import settings


def init_milvus() -> MilvusClient:
    """
    Initialises Milvus (Vector Store DB) connection.

    :returns: MilvusClient
    """
    client = MilvusClient(
        uri=f"{settings.milvus_host}:{settings.milvus_port}",
        user=settings.milvus_username,
        password=settings.milvus_password,
        keep_alive=True,
        db_name=settings.milvus_db_name,
    )
    logger.info("milvus db connected")
    return client


def disconnect_milvus(client: MilvusClient) -> None:
    """
    Disconnects the db connection.

    :param client: requires passing the MilvusClient
    """
    client.close()
    logger.info("milvus db disconnected")
