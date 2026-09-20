from pydantic_settings import BaseSettings, SettingsConfigDict

from tests.tools.config.grpc import GRPCClientTestConfig, GRPCServerTestConfig
from tests.tools.config.http import HTTPClientTestConfig, HTTPServerTestConfig
from tests.tools.config.kafka import KafkaClientTestConfig
from tests.tools.config.postgres import PostgresClientTestConfig


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

    mock_http_server: HTTPServerTestConfig
    mock_grpc_server: GRPCServerTestConfig

    gateway_http_client: HTTPClientTestConfig
    gateway_grpc_client: GRPCClientTestConfig

    operations_http_client: HTTPClientTestConfig
    operations_grpc_client: GRPCClientTestConfig
    operations_kafka_client: KafkaClientTestConfig
    operations_postgres_client: PostgresClientTestConfig

    operations_processing_wait_timeout: float
    """
    Таймаут ожидания асинхронной обработки операций.

    Используется в event-driven тестах для ожидания
    обработки событий перед синхронными проверками.
    """


test_settings = TestSettings()
