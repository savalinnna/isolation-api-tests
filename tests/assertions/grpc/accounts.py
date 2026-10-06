import allure

from contracts.services.accounts.account_pb2 import Account
from tests.assertions.base import assert_equal
from tests.tools.logger import get_test_logger

logger = get_test_logger("ACCOUNTS_ASSERTIONS")


@allure.step("Check account")
def assert_account(actual: Account, expected: Account) -> None:
    logger.info("Check account")

    assert_equal(actual.id, expected.id, "id")
    assert_equal(actual.type, expected.type, "type")
    assert_equal(actual.status, expected.status, "status")
    assert_equal(actual.user_id, expected.user_id, "user_id")
    assert_equal(actual.balance, expected.balance, "balance")
