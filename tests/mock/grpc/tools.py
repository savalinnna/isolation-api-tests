from grpc import StatusCode
from grpc.aio import ServicerContext

from tests.context.scenario import Scenario


async def get_scenario_grpc(context: ServicerContext) -> Scenario:
    # В gRPC сценарий передаётся не через HTTP-заголовок,
    # а через metadata вызова.
    #
    # Это прямой архитектурный аналог X-Test-Scenario:
    # сценарий остаётся явным входом системы, просто на другом транспорте.

    metadata = dict(context.invocation_metadata())

    # В мок-сервисе мы используем единый ключ, согласованный со всем стендом:
    # x-test-scenario.
    #
    # Принципиально: мок не должен иметь дефолтного сценария,
    # иначе тесты перестают быть детерминированными и объяснимыми.
    raw = metadata.get("x-test-scenario")
    if not raw:
        # Отсутствие сценария — это ошибка клиента/теста.
        # Мы не продолжаем выполнение RPC и не возвращаем "пустой" ответ,
        # потому что такой ответ скрывает проблему в конфигурации.
        await context.abort(
            StatusCode.INVALID_ARGUMENT,
            "x-test-scenario metadata is required",
        )

    try:
        # Приводим строковое значение к доменному enum’у Scenario.
        # Это важная точка: сценарий должен быть валидным и известным системе.
        return Scenario(raw)
    except ValueError:
        # Неизвестный сценарий — та же категория ошибки, что и отсутствие.
        # Клиент передал значение, которого мок-сервис не понимает.
        await context.abort(
            StatusCode.INVALID_ARGUMENT,
            f"Unknown test scenario: {raw}",
        )
