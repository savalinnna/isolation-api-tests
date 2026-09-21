from typing import Annotated

from fastapi import Header, HTTPException, status

from tests.context.scenario import Scenario


def get_scenario_http(
    scenario: Annotated[Scenario | None, Header(alias="X-Test-Scenario")] = None
) -> Scenario:
    # Сценарий передаётся в каждом HTTP-запросе через заголовок.
    # Это сознательное архитектурное решение:
    # сценарий является явным входом системы, а не скрытым состоянием.
    #
    # Мы извлекаем сценарий на уровне транспорта,
    # чтобы бизнес-код моков не знал,
    # откуда и каким образом он был передан.

    if not scenario:
        # Отсутствие сценария — это не "пустой кейс",
        # а ошибка конфигурации теста или клиента.
        #
        # Мок-сервис не пытается угадать сценарий
        # и не использует значения по умолчанию,
        # чтобы сохранить детерминизм и предсказуемость поведения.
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="X-Test-Scenario header is required",
        )

    # Возвращаем валидный сценарий,
    # который дальше используется как единственный ключ
    # для выбора поведения мок-сервиса и данных ответа.
    return scenario
