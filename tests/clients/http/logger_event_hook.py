from logging import Logger

from httpx import Request, Response


class HTTPLoggerEventHook:
    """
    Инфраструктурный обработчик событий HTTP-клиента.

    Используется для логирования запросов и ответов
    на уровне транспортного слоя.

    Этот класс не знает:
    - какой тест выполняется,
    - какой сервис вызывается,
    - какие данные передаются.

    Его задача — зафиксировать факт HTTP-взаимодействия
    в логах тестового окружения.
    """

    def __init__(self, logger: Logger):
        # Логгер передаётся извне, чтобы:
        # - не хардкодить источник логов,
        # - использовать единый механизм логирования тестового слоя,
        # - управлять уровнем логов централизованно.
        self.logger = logger

    def request(self, request: Request):
        # Вызывается httpx перед отправкой HTTP-запроса.
        #
        # Мы логируем только метод и URL,
        # не трогая тело запроса и заголовки,
        # чтобы не засорять логи и не утекали чувствительные данные.
        self.logger.info(
            f"{request.method} {request.url} - Waiting for response"
        )

    def response(self, response: Response):
        # Вызывается httpx после получения ответа.
        #
        # В логах мы связываем ответ с исходным запросом
        # и фиксируем HTTP-статус.
        request = response.request
        self.logger.info(
            f"{request.method} {request.url} - Status {response.status_code}"
        )
