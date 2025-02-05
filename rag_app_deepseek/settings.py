import enum
from pathlib import Path
from tempfile import gettempdir
from typing import Optional

from pydantic_settings import BaseSettings

TEMP_DIR = Path(gettempdir())


class LogLevel(str, enum.Enum):  # noqa: WPS600
    """Possible log levels."""

    NOTSET = "NOTSET"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    FATAL = "FATAL"


class Settings(BaseSettings):
    """
    Application settings.

    These parameters can be configured
    with environment variables.
    """

    host: str = "127.0.0.1"
    port: int = 8000
    # quantity of workers for uvicorn
    workers_count: int = 1
    # Enable uvicorn reloading
    reload: bool = False

    # Current environment
    environment: str = "dev"

    log_level: LogLevel = LogLevel.INFO

    kafka_bootstrap_servers: str = "localhost:19092"
    kafka_ssl: bool = False
    kafka_sasl_username: Optional[str] = None
    kafka_sasl_password: Optional[str] = None
    kafka_sasl_mechanism: str = "PLAIN"
    kafka_topic_text: str = "rag-text-local"

    ollama_host: str = "localhost:11434"
    ollama_model: str = "deepseek-r1:32b"

    milvus_conn_name: str = "rag_app_deepseek"
    milvus_host: str = "localhost"
    milvus_port: str = "19530"
    milvus_username: str = ""
    milvus_password: str = ""
    milvus_db_name: str = "default"

    @property
    def kafka_bootstrap_servers_list(self) -> list[str]:
        """
        Kafka bootstrap servers as list.

        :return: list of kafka bootstrap servers.
        """
        return self.kafka_bootstrap_servers.split(",")

    class Config:
        env_file = ".env"
        env_prefix = ""
        env_file_encoding = "utf-8"


settings = Settings()
