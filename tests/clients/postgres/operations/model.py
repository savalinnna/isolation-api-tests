import uuid
from datetime import datetime

from sqlalchemy import Column, UUID, DateTime, Float, String
from sqlalchemy.orm import Mapped

from tests.clients.postgres.base import BaseTestModel


class OperationsTestModel(BaseTestModel):
    """
    ORM-модель таблицы operations в Postgres.

    Важный принцип курса:
    - мы не придумываем структуру данных;
    - мы отражаем реальную схему таблицы в тестовом стенде.

    Эта модель описывает "как операция хранится в БД"
    в рамках стенда, чтобы тестовый слой мог
    подготовить состояние для проверок синхронных API.

    При необходимости сверяйтесь с pgAdmin:
    таблица operations — источник правды
    по именам полей и типам колонок.
    """

    # Имя таблицы в БД. Оно должно совпадать с тем,
    # как таблица реально называется в Postgres.
    __tablename__ = "operations"

    # id операции. В тестах мы часто задаём UUID сами,
    # чтобы дальше использовать его в проверках.
    id: Mapped[uuid.UUID] = Column(UUID, nullable=False, primary_key=True)

    # type и status — строковые поля,
    # которые отражают enum-значения домена (purchase/topup и т.п.).
    #
    # Здесь мы не используем SQLAlchemy Enum,
    # потому что тестовый слой не обязан повторять все ORM-решения сервиса.
    # Нам важно хранение и возможность фильтрации/выборки.
    type: Mapped[str] = Column(String(length=50), nullable=False)
    status: Mapped[str] = Column(String(length=50), nullable=False)

    # amount — сумма операции.
    amount: Mapped[float] = Column(Float, nullable=False)

    # user_id / card_id / account_id — связи с сущностями внешнего домена.
    # В рамках тестового слоя это просто UUID-идентификаторы,
    # достаточные для фильтрации и проверки.
    user_id: Mapped[uuid.UUID] = Column(UUID, nullable=False)
    card_id: Mapped[uuid.UUID] = Column(UUID, nullable=False)
    account_id: Mapped[uuid.UUID] = Column(UUID, nullable=False)

    # category — бизнес-атрибут операции (например, merchant category).
    category: Mapped[str] = Column(String(length=50), nullable=False)

    # created_at — время создания операции.
    # В тестах это поле часто нужно, чтобы проверять сортировки
    # или просто иметь реалистичные данные.
    created_at: Mapped[datetime] = Column(DateTime, nullable=False)
