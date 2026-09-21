from typing import Any

import allure

from tests.tools.logger import get_test_logger

# Единый логгер для всех базовых проверок.
# Это позволяет в логах быстро отследить, что падение произошло
# именно на уровне ассертов, а не в клиенте или сценарии.
logger = get_test_logger("BASE_ASSERTIONS")


@allure.step("Check that {name} equals to {expected}")
def assert_equal(actual: Any, expected: Any, name: str):
    """
    Базовая проверка равенства с инфраструктурной обвязкой.

    Эта функция выполняет ту же проверку, что и обычный assert,
    но дополняет её тремя важными вещами:

    1) Allure step — чтобы проверка была видна в отчёте как отдельный шаг,
       а не как «тест упал где-то внутри».
    2) Логирование — чтобы проверка оставляла читаемый след в логах.
    3) Диагностическое сообщение — чтобы при падении было сразу понятно,
       какое поле проверялось и какие значения ожидались.
    """
    logger.info(f'Check that "{name}" equals to {expected}')

    assert actual == expected, (
        f'Incorrect value: "{name}". '
        f'Expected value: {expected}. '
        f'Actual value: {actual}'
    )
