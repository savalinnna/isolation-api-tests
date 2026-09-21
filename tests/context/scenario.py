from enum import StrEnum


class Scenario(StrEnum):
    """
    Контракт поддерживаемых тестовых сценариев.

    Сценарий в рамках курса — это строка, которая передаётся
    в запросах к gateway-service через заголовок.

    Смысл сценария не в "бизнес-логике" gateway.
    Gateway только транслирует контекст дальше в интеграции.

    Будущий mock-сервер будет читать этот сценарий из заголовка
    и использовать его как ключ для выбора нужных мок-данных.
    """
    USER_WITH_ACTIVE_DEBIT_CARD_ACCOUNT = "user_with_active_debit_card_account"
    USER_WITH_ACTIVE_CREDIT_CARD_ACCOUNT = "user_with_active_credit_card_account"
