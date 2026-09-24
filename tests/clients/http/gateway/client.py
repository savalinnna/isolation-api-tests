import uuid

import allure
from httpx import Response

from tests.clients.http.client import HTTPTestClient, build_http_test_client
from tests.config import test_settings
from tests.context.base import RequestContext
from tests.schema.gateway import (
    GetUserDetailsResponseTestSchema,
    GetAccountDetailsResponseTestSchema,
)
from tests.tools.fakers import fake
from tests.tools.logger import get_test_logger
from tests.tools.routes import APITestRoutes


class GatewayHTTPTestClient(HTTPTestClient):
    """
    HTTP API-клиент тестового слоя для gateway-service.

    Это специализированный клиент, построенный поверх HTTPTestClient.
    Он знает HTTP-контракт gateway-service (пути и ответы), но остаётся
    тестовым инструментом, а не частью бизнес-логики системы.

    Ключевой смысл этого клиента в курсе:
    тест обращается к gateway-service, а gateway-service "под капотом"
    обращается к внешним интеграциям (users/cards/accounts),
    которые в изоляционном контуре подменены мок-сервисами.

    Поэтому входные идентификаторы (user_id / account_id) в этих вызовах
    не являются управляющим параметром поведения — поведение определяется
    сценарным контекстом (RequestContext -> x-test-scenario).
    """

    @allure.step("Get user details")
    def get_user_details_api(
        self,
        user_id: uuid.UUID,
        context: RequestContext,
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
            f"{APITestRoutes.GATEWAY}/user-details/{user_id}",
            context=context,
        )

    @allure.step("Get account details")
    def get_account_details_api(
        self,
        account_id: uuid.UUID,
        context: RequestContext,
    ) -> Response:
        return self.get(
            f"{APITestRoutes.GATEWAY}/account-details/{account_id}",
            context=context,
        )

    def get_user_details(self, context: RequestContext) -> GetUserDetailsResponseTestSchema:
        # Здесь мы сознательно не передаём "реальный" user_id.
        #
        # Почему это корректно:
        # - gateway-service ожидает id в URL, это часть его контракта;
        # - но в нашей архитектуре изоляционных тестов внешний мир
        #   (users/cards/accounts) моделируется по сценарию;
        # - значит, детерминированность достигается не "подбором id",
        #   а явной установкой x-test-scenario.
        #
        # ID здесь нужен только для соблюдения сигнатуры и маршрута.
        response = self.get_user_details_api(fake.uuid(), context)

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

        # Преобразуем JSON-ответ gateway-service в типизированную
        # Pydantic-схему тестового слоя.
        #
        # Здесь фиксируется контракт на уровне тестов:
        # структура ответа должна быть доменно корректной,
        # иначе тест падает на валидации.
        return GetUserDetailsResponseTestSchema.model_validate_json(response.text)

    def get_account_details(self, context: RequestContext) -> GetAccountDetailsResponseTestSchema:
        response = self.get_account_details_api(fake.uuid(), context)
        response.raise_for_status()
        return GetAccountDetailsResponseTestSchema.model_validate_json(response.text)


def build_gateway_http_test_client() -> GatewayHTTPTestClient:
    # Фабрика строит специализированный клиент так же,
    # как и остальные клиенты тестового слоя:
    # - конфигурация берётся из test_settings,
    # - логгер создаётся единым способом,
    # - транспорт настраивается в build_http_test_client.
    #
    # Таким образом, все сервисные клиенты наследуют единое
    # поведение транспорта: base_url, timeout, event hooks, логи.
    client = build_http_test_client(
        logger=get_test_logger("GATEWAY_HTTP_TEST_CLIENT"),
        config=test_settings.gateway_http_client,
    )
    return GatewayHTTPTestClient(client=client)
