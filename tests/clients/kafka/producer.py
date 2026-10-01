import logging

import allure
from confluent_kafka import Producer

from tests.tools.config.kafka import KafkaClientTestConfig


class KafkaProducerTestClient:
    """
    Kafka producer тестового слоя.

    Этот клиент отвечает исключительно за публикацию сообщений
    в Kafka-топики в рамках тестов.

    Важная архитектурная позиция курса:
    - тест инициирует бизнес-флоу через событие;
    - обработка события и бизнес-логика происходят
      на стороне сервисов (consumer'ов);
    - тестовый код не читает Kafka и не содержит consumer'ов.

    Таким образом, KafkaProducerTestClient — это
    инфраструктурный инструмент запуска event-driven сценариев,
    а не часть бизнес-логики тестов.
    """

    def __init__(
        self,
        config: KafkaClientTestConfig,
        logger: logging.Logger,
    ):
        # Логгер передаётся извне, чтобы:
        # - использовать единый механизм логирования тестового слоя;
        # - управлять форматами и уровнями логов централизованно;
        # - не хардкодить инфраструктурные детали в клиенте.
        self.logger = logger

        # Producer инициализируется с минимальной конфигурацией.
        #
        # В тестовом стенде нас интересует не тонкая настройка Kafka,
        # а корректная и детерминированная доставка сообщений
        # в локально контролируемый брокер.
        self.producer = Producer(
            {
                "bootstrap.servers": config.bootstrap_servers,
            }
        )

    @allure.step("Produce message to topic {topic}")
    def produce(self, topic: str, value: str | bytes):
        """
        Публикация одного сообщения в Kafka-топик.

        Бизнес-смысл метода:
        - тест публикует событие;
        - сервис-processor читает его как consumer;
        - далее запускается асинхронный бизнес-флоу.

        Клиент не знает:
        - структуру события;
        - бизнес-смысл payload;
        - кто именно и когда обработает сообщение.
        """
        try:
            # Отправляем сообщение в Kafka.
            #
            # Producer работает асинхронно, поэтому produce()
            # только ставит сообщение в очередь на отправку.
            self.producer.produce(topic, value)

            # poll(0) позволяет обработать внутренние события producer'а:
            # подтверждения доставки, ошибки и т.д.
            #
            # Это минимальный и достаточный вызов для тестового сценария.
            self.producer.poll(0)

            self.logger.info(f"Kafka message produced {topic}")
        except Exception as error:
            # В случае ошибки логируем контекст
            # и пробрасываем исключение выше.
            #
            # Если сообщение не было опубликовано,
            # тест должен падать явно и сразу.
            self.logger.exception(f"Kafka produce failed {topic}:{error}")
            raise

    @allure.step("Flush all messages")
    def flush_all(self, timeout: float = 10.0):
        """
        Принудительное ожидание отправки всех сообщений.

        Этот метод используется в тестах, где важно гарантировать,
        что все события были доставлены в Kafka
        до выполнения последующих шагов (например, чтения через API).

        flush — это синхронизационная точка между
        асинхронным миром Kafka и детерминированным тестом.
        """
        self.logger.info("Kafka producer flush started")
        self.producer.flush(timeout=timeout)
        self.logger.info("Kafka producer flush finished")
