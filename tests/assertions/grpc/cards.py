import allure

from contracts.services.cards.card_pb2 import Card
from tests.assertions.base import assert_equal
from tests.tools.logger import get_test_logger

logger = get_test_logger("CARDS_ASSERTIONS")


@allure.step("Check card")
def assert_card(actual: Card, expected: Card) -> None:
    logger.info("Check card")

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
