from tests.clients.postgres.session import get_postgres_test_session_factory
from tests.config import test_settings

# Фабрика сессий именно для Postgres базы operations-service.
#
# Архитектурный смысл:
# - базовая фабрика сессий универсальна;
# - конфигурация подключения зависит от сервиса;
# - тесты и репозитории не должны читать .env напрямую.
#
# Мы фиксируем подключение один раз в этом модуле
# и переиспользуем его во всех репозиториях operations.
operations_test_session_factory = get_postgres_test_session_factory(
    test_settings.operations_postgres_client,
)
