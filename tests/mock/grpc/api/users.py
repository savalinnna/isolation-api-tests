from pathlib import Path

from grpc.aio import ServicerContext

from contracts.services.users.rpc_get_user_pb2 import GetUserRequest, GetUserResponse
from contracts.services.users.users_service_pb2_grpc import UsersServiceServicer
from tests.mock.grpc.tools import get_scenario_grpc
from tests.tools.logger import get_test_logger
from tests.tools.mock import MockLoader

# MockLoader — инфраструктурный компонент, общий для всех моков.
# Он инкапсулирует:
# - загрузку мок-данных из файлов,
# - валидацию/преобразование в целевую модель ответа,
# - логирование процесса загрузки.
#
# Loader не знает, кто является клиентом (gateway или тест),
# не знает, почему выбран сценарий,
# и не реализует никакой бизнес-логики.
loader = MockLoader(
    root=Path("./tests/mock/grpc/data/users"),
    logger=get_test_logger("USERS_SERVICE_MOCK_LOADER")
)


class UsersMockService(UsersServiceServicer):
    async def GetUser(self, request: GetUserRequest, context: ServicerContext) -> GetUserResponse:
        # request принимается строго по контракту protobuf.
        # Он содержит параметры вызова (например, идентификатор пользователя),
        # но мок-сервис не использует их для вычисления ответа.
        #
        # Это сознательное архитектурное решение:
        # мок моделирует состояние внешнего мира, а не "логику поиска".
        # Вариативность поведения определяется исключительно сценарием.

        scenario = await get_scenario_grpc(context)

        # Имя файла формируется из сценария.
        # Данные хранятся декларативно, в JSON,
        # что позволяет:
        # - переиспользовать сценарии между тестами,
        # - воспроизводить ошибки и edge cases,
        # - держать код мока максимально простым и предсказуемым.
        return await loader.load_grpc(
            file=f"GetUser/{scenario}.json",
            model=GetUserResponse
        )
