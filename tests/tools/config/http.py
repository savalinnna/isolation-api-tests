from pydantic import BaseModel, HttpUrl, IPvAnyAddress


class HTTPServerTestConfig(BaseModel):
    port: int
    address: IPvAnyAddress

class HTTPClientTestConfig(BaseModel):
    """
    Конфигурация HTTP-клиента в тестовом окружении.

    Используется всеми HTTP-клиентами тестового слоя.
    """

    url: HttpUrl
    timeout: float = 120.0
