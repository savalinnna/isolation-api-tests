from enum import StrEnum


class APITestRoutes(StrEnum):
    """
    Контрактное описание API-путей тестируемой системы.

    Используется в:
    - HTTP API-клиентах,
    - mock-серверах,
    - тестах и проверках.

    Централизация роутингов позволяет
    избежать хардкода и расхождений
    между разными частями тестового проекта.
    """
    USERS = '/api/v1/users'
    CARDS = '/api/v1/cards'
    GATEWAY = '/api/v1/gateway'
    ACCOUNTS = '/api/v1/accounts'
    OPERATIONS = '/api/v1/operations'
