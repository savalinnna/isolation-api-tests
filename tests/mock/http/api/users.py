import uuid
from pathlib import Path

from fastapi import APIRouter, Depends

from tests.context.scenario import Scenario
from tests.mock.http.tools import get_scenario_http
from tests.schema.users import GetUserResponseTestSchema
from tests.tools.logger import get_test_logger
from tests.tools.mock import MockLoader
from tests.tools.routes import APITestRoutes

# MockLoader — инфраструктурный компонент.
# Его ответственность строго ограничена:
# - загрузить мок-данные из файлов,
# - провалидировать их контрактом,
# - залогировать процесс загрузки.
#
# Loader не знает:
# - кто вызывает мок (gateway, тест, другой сервис),
# - зачем используется конкретный сценарий,
# - как устроена бизнес-логика системы.
loader = MockLoader(
    root=Path("./tests/mock/http/data/users"),
    logger=get_test_logger("USERS_SERVICE_MOCK_LOADER")
)

# Роутер представляет HTTP-контракт users-service.
# Префикс и пути соответствуют контрактам тестового стенда,
# а не внутренней реализации мок-сервиса.
users_mock_router = APIRouter(
    prefix=APITestRoutes.USERS,
    tags=[APITestRoutes.USERS]
)


@users_mock_router.get("/{user_id}", response_model=GetUserResponseTestSchema)
async def get_user_view(
    user_id: uuid.UUID,
    scenario: Scenario = Depends(get_scenario_http),
):
    # user_id присутствует в сигнатуре,
    # чтобы полностью соответствовать контракту users-service.
    #
    # Важно: мок не использует user_id для вычислений.
    # Поведение мока определяется только сценарием,
    # что гарантирует детерминизм и воспроизводимость тестов.

    return await loader.load_http(
        # Имя файла формируется на основе сценария.
        # Это связывает внешний мир с тестовым сценарием,
        # а не с параметрами конкретного запроса.
        file=f"get_user/{scenario}.json",

        # Ответ валидируется тестовой схемой,
        # что гарантирует контрактную корректность мока.
        model=GetUserResponseTestSchema
    )
