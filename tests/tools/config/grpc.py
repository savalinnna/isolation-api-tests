from pydantic import BaseModel, IPvAnyAddress


class GRPCClientTestConfig(BaseModel):
    """
    Конфигурация gRPC-клиента в тестовом окружении.

    Описывает сетевые параметры подключения
    к gRPC-сервису, независимо от конкретного клиента.
    """

    port: int
    address: IPvAnyAddress

    @property
    def url(self):
        """
        Полный адрес gRPC-сервиса в формате host:port.

        Используется при инициализации gRPC-канала.
        """
        return f"{self.address}:{self.port}"
