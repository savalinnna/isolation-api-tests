from enum import StrEnum


class AllureTag(StrEnum):
    """
    Теги Allure, описывающие технический и архитектурный контекст теста.

    Используются для группировки тестов по:
    - протоколу (HTTP, gRPC, Kafka, Postgres),
    - сервисной зоне (gateway, operations).

    Теги не описывают бизнес-сценарий.
    Их задача — дать быстрый ответ на вопрос:
    "в каком техническом контексте выполняется тест".
    """
    GRPC = "GRPC"
    HTTP = "HTTP"
    KAFKA = "KAFKA"
    POSTGRES = "POSTGRES"

    GATEWAY_SERVICE = "GATEWAY_SERVICE"
    OPERATIONS_SERVICE = "OPERATIONS_SERVICE"


class AllureStory(StrEnum):
    """
    Story в Allure отражает конкретный сценарий
    или пользовательское действие, которое проверяется тестом.

    Story отвечает на вопрос:
    "что именно делает пользователь или система".
    """
    OPERATION_EVENTS = "Operation Events"
    OPERATION_FILTERS = "Operation Filters"

    GET_USER_DETAILS = "Get User Details"
    GET_ACCOUNT_DETAILS = "Get Account Details"


class AllureFeature(StrEnum):
    """
    Feature описывает функциональную область системы.

    Feature отвечает на вопрос:
    "какую часть системы мы сейчас тестируем".
    """
    GATEWAY_SERVICE = "Gateway Service"
    OPERATIONS_SERVICE = "Operations Service"
