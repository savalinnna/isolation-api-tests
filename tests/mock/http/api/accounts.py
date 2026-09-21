import uuid
from pathlib import Path

from fastapi import APIRouter, Depends

from tests.context.scenario import Scenario
from tests.mock.http.tools import get_scenario_http
from tests.schema.accounts import GetAccountResponseTestSchema, GetAccountsResponseTestSchema
from tests.tools.logger import get_test_logger
from tests.tools.mock import MockLoader
from tests.tools.routes import APITestRoutes

loader = MockLoader(
    root=Path("./tests/mock/http/data/accounts"),
    logger=get_test_logger("ACCOUNTS_SERVICE_MOCK_LOADER")
)

accounts_mock_router = APIRouter(
    prefix=APITestRoutes.ACCOUNTS,
    tags=[APITestRoutes.ACCOUNTS]
)


@accounts_mock_router.get("", response_model=GetAccountsResponseTestSchema)
async def get_accounts_view(
    scenario: Scenario = Depends(get_scenario_http),
):
    return await loader.load_http(
        file=f"get_accounts/{scenario}.json",
        model=GetAccountsResponseTestSchema
    )


@accounts_mock_router.get("/{account_id}", response_model=GetAccountResponseTestSchema)
async def get_account_view(
    account_id: uuid.UUID,
    scenario: Scenario = Depends(get_scenario_http),
):
    return await loader.load_http(
        file=f"get_account/{scenario}.json",
        model=GetAccountResponseTestSchema
    )