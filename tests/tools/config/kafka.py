from pydantic import BaseModel, IPvAnyAddress


class KafkaClientTestConfig(BaseModel):
    """
    Конфигурация Kafka-клиента для тестов.

    Используется при публикации событий
    в event-driven сценариях.
    """

    port: int = 9092
    address: IPvAnyAddress

    @property
    def bootstrap_servers(self) -> str:
        """
        Адрес Kafka-брокера в формате host:port.

        Используется Kafka-продьюсерами в тестах.
        """
        return f"{self.address}:{self.port}"
