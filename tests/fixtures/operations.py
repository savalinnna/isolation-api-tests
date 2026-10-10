import pytest

# gRPC API-клиент operations-service тестового слоя.
# Используется для чтения операций через синхронный gRPC API.
from tests.clients.grpc.operations.client import (
    build_operations_grpc_test_client,
    OperationsGRPCTestClient,
)

# HTTP API-клиент operations-service тестового слоя.
# Архитектурно симметричен gRPC-клиенту и используется в HTTP-сценариях.
from tests.clients.http.operations.client import (
    build_operations_http_test_client,
    OperationsHTTPTestClient,
)

# Kafka producer тестового слоя для публикации событий об операциях.
# Через него тест инициирует event-driven флоу.
from tests.clients.kafka.operations.producer import (
    OperationsKafkaProducerTestClient,
    build_operations_kafka_producer_test_client,
)

# Репозиторий тестового слоя для работы с Postgres.
# Используется для проверки состояния хранилища в event-driven тестах.
from tests.clients.postgres.operations.repository import (
    OperationsPostgresTestRepository,
    get_operations_postgres_test_repository,
)


@pytest.fixture
def operations_http_test_client() -> OperationsHTTPTestClient:
    # Инфраструктурная фикстура для HTTP API-клиента operations-service.
    #
    # Фикстура:
    # - не управляет сценарием;
    # - не выполняет запросы;
    # - не содержит бизнес-логики.
    #
    # Она лишь предоставляет тесту готовый инструмент
    # для взаимодействия с HTTP API operations-service.
    return build_operations_http_test_client()


@pytest.fixture
def operations_grpc_test_client() -> OperationsGRPCTestClient:
    # Инфраструктурная фикстура для gRPC API-клиента operations-service.
    #
    # Используется в сценариях, где операции читаются по gRPC.
    # По архитектурной роли полностью симметрична HTTP-фикстуре.
    return build_operations_grpc_test_client()


@pytest.fixture
def operations_postgres_test_repository() -> OperationsPostgresTestRepository:
    # Фикстура для доступа к Postgres в event-driven тестах.
    #
    # Репозиторий используется для сидинга контролируемого состояния БД перед тестом.
    return get_operations_postgres_test_repository()

@pytest.fixture
def operations_kafka_producer_test_client() -> OperationsKafkaProducerTestClient:
    # Фикстура для Kafka producer тестового слоя.
    #
    # Через этот клиент тест публикует события,
    # инициируя асинхронный процессинг операций.
    return build_operations_kafka_producer_test_client()
