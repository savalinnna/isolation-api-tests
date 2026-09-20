from pydantic import ConfigDict, UUID4, BaseModel
from pydantic.alias_generators import to_camel

from tests.types.accounts import AccountTestType, AccountTestStatus


class AccountTestSchema(BaseModel):
    """
    Тестовая схема банковского счёта.
    """

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )

    id: UUID4
    type: AccountTestType
    status: AccountTestStatus
    user_id: UUID4
    balance: float


class GetAccountResponseTestSchema(BaseModel):
    """
    Схема ответа API при получении счёта.
    """

    account: AccountTestSchema


class GetAccountsResponseTestSchema(BaseModel):
    """
    Схема ответа API при получении списка счетов.
    """

    accounts: list[AccountTestSchema]
