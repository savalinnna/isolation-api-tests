import uuid

import allure
from httpx import Response, QueryParams

from tests.clients.http.client import HTTPTestClient, build_http_test_client
from tests.config import test_settings
from tests.schema.operations import (
   GetOperationResponseTestSchema,
   GetOperationsQueryTestSchema,
   GetOperationsResponseTestSchema,
)
from tests.tools.logger import get_test_logger
from tests.tools.routes import APITestRoutes


class OperationsHTTPTestClient(HTTPTestClient):
    """
    HTTP API-клиент тестового слоя для operations-service.

    Это специализированный клиент, построенный поверх HTTPTestClient.
    Он знает HTTP-контракт operations-service (пути и ответы), но остаётся
    тестовым инструментом, а не частью бизнес-логики системы.

    Ключевой смысл этого клиента в курсе:
    тест обращается к operations-service, а operations-service "под капотом"
    обращается к внешним интеграциям (users/cards/accounts),
    которые в изоляционном контуре подменены мок-сервисами.

    Поэтому входные идентификаторы (user_id / account_id) в этих вызовах
    не являются управляющим параметром поведения — поведение определяется
    сценарным контекстом (RequestContext -> x-test-scenario).
    """

    @allure.step("Get operation")
    def get_operation_api(
            self,
            operation_id: uuid.UUID
    ) -> Response:
        # Низкоуровневый метод "api" возвращает сырой Response.
        #
        # Он нужен как строительный блок: если тесту потребуется
        # отдельная диагностика статусов / заголовков / raw текста,
        # это можно сделать на уровне Response.
        #
        # Важно: context обязателен, потому что эти ручки gateway
        # в рамках изоляционных тестов управляются сценарием.
        return self.get(
            f"{APITestRoutes.OPERATIONS}/{operation_id}",
        )

    @allure.step("Get operations")
    def get_operations_api(
            self,
            query: GetOperationsQueryTestSchema
    ) -> Response:
        return self.get(
            APITestRoutes.OPERATIONS,
            params=QueryParams(**query.model_dump(by_alias=True, exclude_none=True))
        )

    def get_operation(
            self,
            operation_id: uuid.UUID
    ) -> GetOperationResponseTestSchema:
        # Здесь мы сознательно не передаём "реальный" operation_id.
        #
        # Почему это корректно:
        # - operations-service ожидает id в URL, это часть его контракта;
        # - но в нашей архитектуре изоляционных тестов внешний мир
        #   (users/cards/accounts) моделируется по сценарию;
        # - значит, детерминированность достигается не "подбором id",
        #   а явной установкой x-test-scenario.
        #
        # ID здесь нужен только для соблюдения сигнатуры и маршрута.
        response = self.get_operation_api(operation_id)

        # Мы намеренно делаем raise_for_status() внутри фасадного метода.
        #
        # Это сознательное упрощение ради фокуса курса:
        # - если статус неуспешный, тест должен падать сразу и явно;
        # - затем мы валидируем успешный ответ доменной схемой.
        #
        # Альтернативный подход (тоже корректный):
        # - вернуть Response в тест,
        # - явно проверить статус через ассерты,
        # - и только затем валидировать модель.
        #
        # В курсе мы не размываем внимание протокольными проверками,
        # а фокусируемся на изоляции и сценарной воспроизводимости.
        response.raise_for_status()

        # Преобразуем JSON-ответ operations-service в типизированную
        # Pydantic-схему тестового слоя.
        #
        # Здесь фиксируется контракт на уровне тестов:
        # структура ответа должна быть доменно корректной,
        # иначе тест падает на валидации.
        return GetOperationResponseTestSchema.model_validate_json(response.text)

    def get_operations(
            self,
            user_id: uuid.UUID,
            card_id: uuid.UUID | None = None,
            account_id: uuid.UUID | None = None,
    ) -> GetOperationsResponseTestSchema:
        query = GetOperationsQueryTestSchema(
            user_id=user_id,
            card_id=card_id,
            account_id=account_id
        )
        response = self.get_operations_api(query)
        response.raise_for_status()
        return GetOperationsResponseTestSchema.model_validate_json(response.text)


def build_operations_http_test_client() -> OperationsHTTPTestClient:
    # Фабрика строит специализированный клиент так же,
    # как и остальные клиенты тестового слоя:
    # - конфигурация берётся из test_settings,
    # - логгер создаётся единым способом,
    # - транспорт настраивается в build_http_test_client.
    #
    # Таким образом, все сервисные клиенты наследуют единое
    # поведение транспорта: base_url, timeout, event hooks, логи.
    client = build_http_test_client(
        logger=get_test_logger("OPERATIONS_HTTP_TEST_CLIENT"),
        config=test_settings.operations_http_client,
    )
    return OperationsHTTPTestClient(client=client)
