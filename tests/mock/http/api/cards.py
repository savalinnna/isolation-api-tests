import uuid
from pathlib import Path

from fastapi import APIRouter, Depends

from tests.context.scenario import Scenario
from tests.mock.http.tools import get_scenario_http
from tests.schema.cards import GetCardResponseTestSchema, GetCardsResponseTestSchema
from tests.tools.logger import get_test_logger
from tests.tools.mock import MockLoader
from tests.tools.routes import APITestRoutes

loader = MockLoader(
    root=Path("./tests/mock/http/data/cards"),
    logger=get_test_logger("CARDS_SERVICE_MOCK_LOADER")
)

cards_mock_router = APIRouter(
    prefix=APITestRoutes.CARDS,
    tags=[APITestRoutes.CARDS]
)


@cards_mock_router.get("", response_model=GetCardsResponseTestSchema)
async def get_cards_view(
    scenario: Scenario = Depends(get_scenario_http),
):
    return await loader.load_http(
        file=f"get_cards/{scenario}.json",
        model=GetCardsResponseTestSchema
    )


@cards_mock_router.get("/{card_id}", response_model=GetCardResponseTestSchema)
async def get_card_view(
    card_id: uuid.UUID,
    scenario: Scenario = Depends(get_scenario_http),
):
    return await loader.load_http(
        file=f"get_card/{scenario}.json",
        model=GetCardResponseTestSchema
    )
