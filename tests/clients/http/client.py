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
        # httpx.Client создаётся снаружи и передаётся в клиент,
        # чтобы:
        # - отделить конфигурацию транспорта от логики вызовов,
        # - переиспользовать клиент между вызовами,
        # - управлять жизненным циклом соединений централизованно.
        self.client = client

    @allure.step("Make GET request to {url}")
    def get(
            self,
            url: str,
            params: QueryParams | None = None,
            context: RequestContext | None = None
    ) -> Response:
        # Заголовки формируются динамически.
        #
        # Если контекст не передан, запрос выполняется без
        # тестового контекста (например, для health-check или
        # вспомогательных вызовов).
        headers = Headers()

        if context:
            # Преобразуем RequestContext в HTTP-заголовки.
            #
            # Важно: клиент не знает, что такое "сценарий".
            # Он просто применяет контракт преобразования контекста
            # в транспортные атрибуты.
            headers = Headers(build_http_test_headers(context))

        # HTTPTestClient не выполняет валидацию ответа
        # и не знает о доменных схемах.
        # Его задача — корректно выполнить HTTP-вызов
        # и вернуть "сырой" Response выше по стеку.
        return self.client.get(
            url=url,
            params=params,
            headers=headers
        )

    def build_http_test_client(
            logger: Logger,
            config: HTTPClientTestConfig
    ) -> Client:
        """
        Фабрика создания httpx.Client для тестового слоя.

        Это единственное место, где:
        - применяется конфигурация HTTP-клиента,
        - настраивается транспортный уровень,
        - подключаются инфраструктурные event hooks.

        Все API-клиенты сервисов используют именно этот Client,
        что гарантирует единое поведение HTTP-взаимодействий
        во всём тестовом проекте.
        """

        # Инициализируем обработчик логирования HTTP-событий.
        #
        # Он будет вызываться httpx автоматически:
        # - перед отправкой запроса,
        # - после получения ответа.
        #
        # Клиенты сервисов не знают о логировании —
        # это инфраструктурная ответственность.
        logger_event_hook = HTTPLoggerEventHook(logger=logger)

        return Client(
            # Таймаут берётся из типизированной конфигурации
            # тестового окружения, а не задаётся в коде.
            timeout=config.timeout,

            # base_url задаёт корень всех HTTP-вызовов клиента.
            # Конкретные API-клиенты работают только с относительными путями,
            # не зная, в какое окружение они направлены.
            base_url=str(config.url),

            # Event hooks подключаются один раз на уровне клиента
            # и автоматически применяются ко всем HTTP-запросам.
            event_hooks={
                "request": [logger_event_hook.request],
                "response": [logger_event_hook.response],
            },
        )
