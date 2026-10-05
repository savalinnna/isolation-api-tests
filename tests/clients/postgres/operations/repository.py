import allure

from tests.clients.postgres.operations.model import OperationsTestModel
from tests.clients.postgres.operations.session import operations_test_session_factory
from tests.clients.postgres.repository import PostgresTestRepository
from tests.tools.fakers import fake
from tests.types.operations import OperationTestType, OperationTestStatus


class OperationsPostgresTestRepository(PostgresTestRepository):
    """
    Репозиторий test-слоя для работы с таблицей operations.

    Его роль — дать тестам доменно-удобные фабричные методы,
    которые создают в БД записи с нужными атрибутами.

    Важный момент:
    это не бизнес-логика и не замена processor'а.
    Мы используем repository только в сценариях,
    где предмет проверки — синхронное API (например, фильтры),
    а не event-driven обработка.
    """

    @allure.step("Create in progress purchase operation")
    def create_in_progress_purchase_operation(self) -> OperationsTestModel:
        """
        Создаёт в БД операцию PURCHASE со статусом IN_PROGRESS.

        Это удобный строитель данных для тестов:
        - фиксирует семантику сценария;
        - убирает ручное заполнение полей из теста;
        - оставляет repository инфраструктурным: он всё ещё только пишет в БД.
        """
        return self.create(
            OperationsTestModel(
                # UUID генерируем детерминированно (в рамках fake),
                # чтобы тест мог опираться на конкретные значения.
                id=fake.uuid(),

                # Тип и статус задаём явно, потому что это часть сценария.
                type=OperationTestType.PURCHASE,
                status=OperationTestStatus.IN_PROGRESS,

                # Остальные поля — реалистичные значения,
                # которые не важны для логики фильтрации,
                # но важны для "живых" данных в тестовом слое.
                amount=fake.amount(),
                user_id=fake.uuid(),
                card_id=fake.uuid(),
                category=fake.category(),
                account_id=fake.uuid(),
                created_at=fake.date_time(),
            )
        )

    @allure.step("Create completed purchase operation")
    def create_completed_purchase_operation(self) -> OperationsTestModel:
        """
        Создаёт в БД завершённую операцию PURCHASE со статусом COMPLETED.

        В дальнейшем такие методы позволят собирать наборы данных
        для тестов фильтрации и выборок:
        например, две операции одного пользователя и одна другого,
        чтобы проверить корректность query-параметров API.
        """
        return self.create(
            OperationsTestModel(
                id=fake.uuid(),
                type=OperationTestType.PURCHASE,
                status=OperationTestStatus.COMPLETED,
                amount=fake.amount(),
                user_id=fake.uuid(),
                card_id=fake.uuid(),
                category=fake.category(),
                account_id=fake.uuid(),
                created_at=fake.date_time(),
            )
        )


def get_operations_postgres_test_repository() -> OperationsPostgresTestRepository:
    """
    Фабрика получения репозитория operations.

    Здесь мы фиксируем композицию:
    - какой session_factory используется;
    - какой repository возвращается.

    Тесты импортируют только эту функцию,
    чтобы не размазывать детали сборки по проекту.
    """
    return OperationsPostgresTestRepository(
        session_factory=operations_test_session_factory
    )
