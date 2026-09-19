import uuid
from datetime import datetime

from faker import Faker
from faker.providers.python import TEnum


class Fake:
    """
    Централизованный генератор тестовых данных.

    Этот класс используется как единая точка генерации
    случайных доменных значений для автотестов:
    идентификаторов, enum'ов, сумм, дат и категорий.

    Тесты не работают напрямую с библиотекой генерации,
    а используют этот фасад.
    """

    def __init__(self, faker: Faker):
        # Внутренний объект генерации данных.
        # Снаружи тесты с ним напрямую не взаимодействуют.
        self.faker = faker

    def uuid(self) -> uuid.UUID:
        """
        Генерирует уникальный идентификатор сущности.

        Используется для:
        - идентификаторов операций
        - идентификаторов счетов
        - идентификаторов карт
        и любых других доменных объектов в тестах.
        """
        return self.faker.uuid4(cast_to=None)

    def enum(self, value: type[TEnum]) -> TEnum:
        """
        Возвращает случайное значение из переданного enum'а.

        Используется вместе с тестовыми доменными enum'ами
        (OperationTestType, CardTestStatus и т.д.),
        чтобы генерировать валидные доменные значения.
        """
        return self.faker.enum(value)

    def category(self) -> str:
        """
        Генерирует категорию операции или платежа.

        Категории заданы явно, чтобы:
        - контролировать доменное пространство значений
        - не зависеть от случайных строк
        - использовать реалистичные бизнес-категории
        """
        return self.faker.random_element([
            "gas",
            "taxi",
            "tolls",
            "water",
            "beauty",
            "mobile",
            "travel",
            "parking",
            "catalog",
            "internet",
            "satellite",
            "education",
            "government",
            "healthcare",
            "restaurants",
            "electricity",
            "supermarkets",
        ])

    def float(self, start: int = 1, end: int = 100) -> float:
        """
        Генерирует числовое значение с плавающей точкой
        в заданном диапазоне.

        Используется как базовый метод для генерации
        числовых доменных значений.
        """
        return self.faker.pyfloat(min_value=start, max_value=end, right_digits=2)

    def amount(self) -> float:
        """
        Генерирует денежную сумму операции.

        Это семантическая обертка над float(),
        чтобы в тестах было явно видно,
        что речь идет именно о сумме денег.
        """
        return self.float(1, 1000)

    def date_time(self) -> datetime:
        """
        Генерирует дату и время доменного события.

        Используется для:
        - времени операции
        - времени создания сущности
        - временных полей в API-запросах и ответах
        """
        return self.faker.date_time()


# Единый экземпляр генератора для всего тестового проекта.
# Импортируется и используется напрямую в тестах и фабриках.
fake = Fake(faker=Faker())
