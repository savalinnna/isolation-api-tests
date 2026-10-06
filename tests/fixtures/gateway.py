import pytest

from tests.clients.grpc.gateway.client import (
    GatewayGRPCTestClient,
    build_gateway_grpc_test_client,
)
from tests.clients.http.gateway.client import (
    GatewayHTTPTestClient,
    build_gateway_http_test_client,
)


@pytest.fixture
def gateway_http_test_client() -> GatewayHTTPTestClient:
    # Фикстура сценарного тестового слоя для HTTP-клиента gateway-service.
    #
    # Эта фикстура:
    # - не знает, какой сценарий будет использовать тест;
    # - не управляет поведением внешних интеграций;
    # - не выполняет HTTP-вызовы сама.
    #
    # Её единственная ответственность — предоставить тесту
    # корректно сконфигурированный HTTP API-клиент gateway-service,
    # через который тест будет взаимодействовать с системой.
    #
    # Все архитектурные решения уже зафиксированы на уровне клиента:
    # - конфигурация окружения берётся из test_settings;
    # - транспорт настроен централизованно;
    # - поддержка RequestContext и сценариев встроена в клиент.
    #
    # Фикстура лишь вызывает фабрику и возвращает готовый инструмент,
    # не вмешиваясь в бизнес-смысл теста.
    return build_gateway_http_test_client()


@pytest.fixture
def gateway_grpc_test_client() -> GatewayGRPCTestClient:
    # Фикстура сценарного тестового слоя для gRPC-клиента gateway-service.
    #
    # По архитектурному смыслу она симметрична HTTP-фикстуре:
    # - предоставляет тесту точку входа в gateway-service по gRPC;
    # - не управляет сценарием и не знает, какие моки будут задействованы;
    # - не содержит логики, связанной с проверками или данными.
    #
    # Разделение HTTP и gRPC клиентов на уровне фикстур сделано намеренно:
    # - протокол выбирается явно в тесте;
    # - сценарии и ассерты остаются одинаковыми;
    # - транспортный слой не смешивается с бизнес-смыслом проверки.
    #
    # Как и в HTTP-случае, вся инициализация вынесена в фабрику,
    # а фикстура остаётся минимальной и декларативной.
    return build_gateway_grpc_test_client()
