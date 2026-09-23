from pathlib import Path

from grpc.aio import ServicerContext

from contracts.services.accounts.accounts_service_pb2_grpc import AccountsServiceServicer
from contracts.services.accounts.rpc_get_account_pb2 import GetAccountRequest, GetAccountResponse
from contracts.services.accounts.rpc_get_accounts_pb2 import GetAccountsRequest, GetAccountsResponse
from tests.mock.grpc.tools import get_scenario_grpc
from tests.tools.logger import get_test_logger
from tests.tools.mock import MockLoader

# Отдельный loader на сервис — это удобная граница ответственности.
# Он фиксирует корень файловой структуры данных accounts-service
# и отдельный логгер, чтобы при отладке было ясно,
# какой именно мок и какие именно данные загружались.
loader = MockLoader(
    root=Path("./tests/mock/grpc/data/accounts"),
    logger=get_test_logger("ACCOUNTS_SERVICE_MOCK_LOADER")
)


class AccountsMockService(AccountsServiceServicer):
    async def GetAccount(self, request: GetAccountRequest, context: ServicerContext) -> GetAccountResponse:
        # request содержит параметры (например, account_id),
        # но мок-сервис не использует их для вычислений.
        # Поведение определяется сценарием, а параметры существуют для контракта.
        scenario = await get_scenario_grpc(context)

        return await loader.load_grpc(
            file=f"GetAccount/{scenario}.json",
            model=GetAccountResponse
        )

    async def GetAccounts(self, request: GetAccountsRequest, context: ServicerContext) -> GetAccountsResponse:
        # Аналогично: список accounts — это часть состояния внешнего мира в сценарии.
        # Мы не фильтруем, не сортируем и не "ищем" accounts по request.
        scenario = await get_scenario_grpc(context)

        return await loader.load_grpc(
            file=f"GetAccounts/{scenario}.json",
            model=GetAccountsResponse
        )