from pathlib import Path

from grpc.aio import ServicerContext

from contracts.services.cards.cards_service_pb2_grpc import CardsServiceServicer
from contracts.services.cards.rpc_get_card_pb2 import GetCardRequest, GetCardResponse
from contracts.services.cards.rpc_get_cards_pb2 import GetCardsRequest, GetCardsResponse
from tests.mock.grpc.tools import get_scenario_grpc
from tests.tools.logger import get_test_logger
from tests.tools.mock import MockLoader

# Отдельный loader на сервис — это удобная граница ответственности.
# Он фиксирует корень файловой структуры данных cards-service
# и отдельный логгер, чтобы при отладке было ясно,
# какой именно мок и какие именно данные загружались.
loader = MockLoader(
    root=Path("./tests/mock/grpc/data/cards"),
    logger=get_test_logger("CARDS_SERVICE_MOCK_LOADER")
)


class CardsMockService(CardsServiceServicer):
    async def GetCard(self, request: GetCardRequest, context: ServicerContext) -> GetCardResponse:
        # request содержит параметры (например, card_id),
        # но мок-сервис не использует их для вычислений.
        # Поведение определяется сценарием, а параметры существуют для контракта.
        scenario = await get_scenario_grpc(context)

        return await loader.load_grpc(
            file=f"GetCard/{scenario}.json",
            model=GetCardResponse
        )

    async def GetCards(self, request: GetCardsRequest, context: ServicerContext) -> GetCardsResponse:
        # Аналогично: список карт — это часть состояния внешнего мира в сценарии.
        # Мы не фильтруем, не сортируем и не "ищем" карты по request.
        scenario = await get_scenario_grpc(context)

        return await loader.load_grpc(
            file=f"GetCards/{scenario}.json",
            model=GetCardsResponse
        )
