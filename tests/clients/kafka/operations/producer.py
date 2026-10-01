import time

import allure

from tests.clients.kafka.producer import KafkaProducerTestClient
from tests.config import test_settings
from tests.schema.operations import OperationEventTestSchema
from tests.tools.logger import get_test_logger
from tests.types.operations import OperationTestType, OperationTestStatus


class OperationsKafkaProducerTestClient(KafkaProducerTestClient):
    """
    Kafka producer тестового слоя для событий operations-service.

    Этот клиент публикует события операций в Kafka-топик,
    который читается operations-processor'ом.

    Важный архитектурный момент:
    - тест публикует событие;
    - operations-processor читает его как consumer;
    - бизнес-логика и сохранение в БД происходят на стороне сервиса;
    - тест проверяет результат через синхронные API.

    Клиент не знает:
    - как именно реализована обработка события;
    - сколько сервисов участвует в цепочке;
    - какие таблицы и структуры используются внутри.
    """

    @allure.step("Produce operation event")
    def produce_operation_event_api(
            self,
            event: OperationEventTestSchema,
    ) -> OperationEventTestSchema:
        """
        Публикация события операции в Kafka.

        Это низкоуровневый API-метод:
        - он отправляет событие в конкретный Kafka-топик;
        - гарантирует доставку сообщения;
        - ждёт завершения обработки на стороне сервиса.

        Метод возвращает само событие,
        чтобы тест мог использовать его как ожидаемую модель данных.
        """
        self.produce(
            topic="operations-service.operation-event.inbox",
            value=event.model_dump_json(),
        )

        # Гарантируем, что сообщение физически отправлено в Kafka.
        self.flush_all()

        # См. подробное пояснение ниже — почему здесь есть sleep
        # и почему это осознанное архитектурное решение.
        time.sleep(test_settings.operations_processing_wait_timeout)

        return event

    @allure.step("Produce in progress purchase operation event")
    def produce_in_progress_purchase_operation_event(self) -> OperationEventTestSchema:
        """
        Публикация события операции покупки со статусом IN_PROGRESS.

        Это фасадный метод, который:
        - фиксирует конкретный бизнес-сценарий;
        - не содержит логики продюсинга;
        - просто формирует корректное событие по контракту.
        """
        return self.produce_operation_event_api(
            OperationEventTestSchema(
                type=OperationTestType.PURCHASE,
                status=OperationTestStatus.IN_PROGRESS
            )
        )

    @allure.step("Produce completed purchase operation event")
    def produce_completed_purchase_operation_event(self) -> OperationEventTestSchema:
        """
        Публикация события завершённой операции покупки.
        """
        return self.produce_operation_event_api(
            OperationEventTestSchema(
                type=OperationTestType.PURCHASE,
                status=OperationTestStatus.COMPLETED
            )
        )


def build_operations_kafka_producer_test_client() -> OperationsKafkaProducerTestClient:
    """
    Фабрика создания Kafka producer для operations-service.

    Как и во всех клиентах тестового слоя:
    - конфигурация берётся из test_settings;
    - логгер создаётся единым способом;
    - клиент не читает .env напрямую.
    """
    return OperationsKafkaProducerTestClient(
        config=test_settings.operations_kafka_client,
        logger=get_test_logger("OPERATIONS_KAFKA_PRODUCER_TEST_CLIENT"),
    )
