import uvicorn
from fastapi import FastAPI

from tests.config import test_settings
from tests.mock.http.api.accounts import accounts_mock_router
from tests.mock.http.api.cards import cards_mock_router
from tests.mock.http.api.users import users_mock_router

# HTTP мок-сервис — это отдельное приложение,
# которое моделирует внешний мир для gateway и других сервисов.
#
# Оно не содержит тестовой логики и не знает,
# кто именно будет его вызывать:
# gateway, автотест или другой компонент стенда.
app = FastAPI(title="mock-service")

# Регистрируем HTTP моки сервисов.
# Каждый роутер соответствует контракту отдельного сервиса
# (users, cards и т.д.).
#
# Сервер не знает ничего о сценариях и данных —
# он лишь объединяет заранее реализованные моки
# в единый HTTP-контур.
app.include_router(users_mock_router)
app.include_router(cards_mock_router)
app.include_router(accounts_mock_router)

if __name__ == "__main__":
    # HTTP мок-сервис запускается как самостоятельный процесс.
    #
    # Адрес и порт берутся из конфигурации тестового окружения,
    # чтобы:
    # - одинаково работать локально и в Docker,
    # - легко переключать окружения,
    # - не хардкодить сетевые параметры в коде.
    #
    # Количество workers выбирается исходя из инфраструктурных
    # требований, а не логики мок-сервиса.
    uvicorn.run(
        app="tests.mock.http.server:app",
        host=str(test_settings.mock_http_server.address),
        port=test_settings.mock_http_server.port,
        workers=3
    )
