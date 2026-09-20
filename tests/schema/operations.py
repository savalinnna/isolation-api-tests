from datetime import datetime

from pydantic import BaseModel, UUID4, Field, ConfigDict
from pydantic.alias_generators import to_camel

from tests.tools.fakers import fake
from tests.types.operations import OperationTestType, OperationTestStatus


class OperationTestSchema(BaseModel):
    """
    Тестовая схема операции.

    Описывает операцию так, как она возвращается
    через синхронное API (HTTP / gRPC).
    """

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )

    id: UUID4
    type: OperationTestType
    status: OperationTestStatus
    amount: float
    user_id: UUID4
    card_id: UUID4
    category: str
    created_at: datetime
    account_id: UUID4


class OperationEventTestSchema(BaseModel):
    """
    Схема события операции.

    Используется для генерации событий,
    которые отправляются в Kafka в тестах.
    """

    type: OperationTestType = Field(default_factory=lambda: fake.enum(OperationTestType))
    status: OperationTestStatus = Field(default_factory=lambda: fake.enum(OperationTestStatus))
    amount: float = Field(default_factory=fake.amount)
    user_id: UUID4 = Field(default_factory=fake.uuid)
    card_id: UUID4 = Field(default_factory=fake.uuid)
    category: str = Field(default_factory=fake.category)
    created_at: datetime = Field(default_factory=fake.date_time)
    account_id: UUID4 = Field(default_factory=fake.uuid)


class GetOperationResponseTestSchema(BaseModel):
    """
    Схема ответа API при получении одной операции.
    """

    operation: OperationTestSchema


class GetOperationsQueryTestSchema(BaseModel):
    """
    Схема query-параметров для запроса списка операций.
    """

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )

    user_id: UUID4
    card_id: UUID4 | None = None
    account_id: UUID4 | None = None


class GetOperationsResponseTestSchema(BaseModel):
    """
    Схема ответа API при получении списка операций.
    """

    operations: list[OperationTestSchema]
