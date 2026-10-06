from logging import Logger

import allure
from httpx import Client, Response, QueryParams, Headers

from tests.clients.http.logger_event_hook import HTTPLoggerEventHook
from tests.context.base import RequestContext, build_http_test_headers
from tests.tools.config.http import HTTPClientTestConfig


class HTTPTestClient:
    """
    Базовый HTTP API-клиент тестового слоя.

    Этот класс инкапсулирует:
    - работу с httpx.Client,
    - прокидывание тестового контекста,
    - базовые HTTP-операции.

    Он не содержит знаний о конкретных сервисах
    и используется как фундамент для специализированных клиентов.
    """

    def __init__(self, client: Client) -> None:
        self.client = client

    @allure.step("Make GET request to {url}")
    def get(
        self,
        url: str,
        params: QueryParams | None = None,
        context: RequestContext | None = None,
    ) -> Response:
        headers = Headers()

        if context:
            headers = Headers(build_http_test_headers(context))

        return self.client.get(
            url=url,
            params=params,
            headers=headers,
        )


def build_http_test_client(
    logger: Logger,
    config: HTTPClientTestConfig,
) -> Client:
    """
    Фабрика создания httpx.Client для тестового слоя.

    Здесь:
    - применяется конфигурация HTTP-клиента,
    - настраивается транспортный уровень,
    - подключаются event hooks.
    """
    logger_event_hook = HTTPLoggerEventHook(logger=logger)

    return Client(
        timeout=config.timeout,
        base_url=str(config.url),
        event_hooks={
            "request": [logger_event_hook.request],
            "response": [logger_event_hook.response],
        },
    )
