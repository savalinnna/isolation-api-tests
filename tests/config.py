from pydantic_settings import BaseSettings, SettingsConfigDict

from tests.tools.config.grpc import GRPCClientTestConfig
from tests.tools.config.http import HTTPClientTestConfig
from tests.tools.config.kafka import KafkaClientTestConfig


class TestSettings(BaseSettings):
    """
    Корневая конфигурация тестового окружения.

    Является единой точкой входа для всех настроек,
    используемых в тестах и клиентах.
    """

    model_config = SettingsConfigDict(
        extra="allow",
        env_file="./tests/.env",
        env_file_encoding="utf-8",
        env_nested_delimiter=".",
    )

    gateway_http_client: HTTPClientTestConfig
    gateway_grpc_client: GRPCClientTestConfig

    operations_http_client: HTTPClientTestConfig
    operations_grpc_client: GRPCClientTestConfig
    operations_kafka_client: KafkaClientTestConfig

    operations_processing_wait_timeout: float
    """
    Таймаут ожидания асинхронной обработки операций.

    Используется в event-driven тестах для ожидания
    обработки событий перед синхронными проверками.
    """


test_settings = TestSettings()
