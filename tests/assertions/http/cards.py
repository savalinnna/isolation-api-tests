import allure

from tests.assertions.base import assert_equal
from tests.schema.cards import CardTestSchema
from tests.tools.logger import get_test_logger

logger = get_test_logger("CARDS_ASSERTIONS")


@allure.step("Check card")
def assert_card(actual: CardTestSchema, expected: CardTestSchema) -> None:
    logger.info("Check card")

    # Карта — самостоятельная доменная сущность внешнего мира,
    # с которой gateway работает исключительно по контракту.
    #
    # Здесь важно, что мы проверяем не "реализацию карты",
    # а те атрибуты, которые имеют бизнес-смысл в интеграционном контуре:
    # тип карты, статус, платёжную систему, срок действия и реквизиты.
    #
    # Проверка каждого поля отдельно позволяет:
    # - быстро понять причину падения теста;
    # - отличить контрактную ошибку от сценарной;
    # - сохранить читаемость ассерта как части сценария.
    assert_equal(actual.id, expected.id, "id")
    assert_equal(actual.pin, expected.pin, "pin")
    assert_equal(actual.cvv, expected.cvv, "cvv")
    assert_equal(actual.type, expected.type, "type")
    assert_equal(actual.status, expected.status, "status")
    assert_equal(actual.account_id, expected.account_id, "account_id")
    assert_equal(actual.card_number, expected.card_number, "card_number")
    assert_equal(actual.card_holder, expected.card_holder, "card_holder")
    assert_equal(actual.expiry_date, expected.expiry_date, "expiry_date")
    assert_equal(actual.payment_system, expected.payment_system, "payment_system")
