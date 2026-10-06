import allure

from tests.assertions.base import assert_equal
from tests.schema.accounts import AccountTestSchema
from tests.tools.logger import get_test_logger

logger = get_test_logger("ACCOUNTS_ASSERTIONS")


@allure.step("Check account")
def assert_account(actual: AccountTestSchema, expected: AccountTestSchema) -> None:
    logger.info("Check account")

    # Счёт — ключевая доменная сущность,
    # через которую gateway агрегирует карты и операции.
    #
    # Именно атрибуты счёта (тип, статус, баланс)
    # определяют бизнес-смысл ответа gateway,
    # поэтому они должны быть явно проверяемы и читаемы.
    #
    # Мы намеренно не используем deep equal и не сравниваем
    # объект целиком, чтобы:
    # - проверка оставалась доменной, а не технической;
    # - отчёт по падению указывал на конкретный нарушенный инвариант;
    # - ассерты можно было переиспользовать в разных сценариях.
    assert_equal(actual.id, expected.id, "id")
    assert_equal(actual.type, expected.type, "type")
    assert_equal(actual.status, expected.status, "status")
    assert_equal(actual.user_id, expected.user_id, "user_id")
    assert_equal(actual.balance, expected.balance, "balance")
