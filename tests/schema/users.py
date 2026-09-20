from pydantic import BaseModel, ConfigDict, UUID4, EmailStr
from pydantic.alias_generators import to_camel


class UserTestSchema(BaseModel):
    """
    Тестовая схема пользователя.

    Используется для описания пользователя
    так, как он виден через API и контракты,
    а не как он хранится внутри сервиса.
    """

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )

    id: UUID4
    email: EmailStr
    last_name: str
    first_name: str
    middle_name: str
    phone_number: str


class GetUserResponseTestSchema(BaseModel):
    """
    Схема ответа API при получении пользователя.
    """

    user: UserTestSchema
