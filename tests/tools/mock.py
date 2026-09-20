from logging import Logger
from pathlib import Path
from typing import TypeVar, Type

import aiofiles
from google.protobuf.json_format import Parse
from google.protobuf.message import Message
from pydantic import BaseModel

# Тип переменной для HTTP-моков.
# Ограничиваемся Pydantic-моделями,
# потому что HTTP-контракты в курсе описываются через Pydantic.
HTTPModelT = TypeVar("HTTPModelT", bound=BaseModel)

# Тип переменной для gRPC-моков.
# Здесь мы работаем с protobuf-сообщениями.
GRPCModelT = TypeVar("GRPCModelT", bound=Message)


class MockLoader:
    """
    Централизованный механизм загрузки мок-данных.

    Этот класс отвечает за:
    - чтение моковых JSON-файлов с диска,
    - логирование процесса загрузки,
    - валидацию данных контрактами (Pydantic / Protobuf).

    MockLoader не знает:
    - для какого сервиса используется мок,
    - в каком тесте или сценарии он применяется,
    - будет ли он использован в mock-сервере или напрямую в тесте.

    Его задача — быть единственной точкой,
    где мок-данные переходят из "файла" в "валидный объект".
    """

    def __init__(self, root: Path, logger: Logger):
        # Корневая директория, в которой лежат мок-файлы.
        # Это позволяет гибко управлять структурой моков:
        # по сервисам, сценариям или версиям контрактов.
        self.root = root

        # Логгер передаётся снаружи,
        # чтобы MockLoader не диктовал стратегию логирования.
        self.logger = logger

    async def get_raw_data(self, file: str) -> str:
        """
        Загружает сырое содержимое мок-файла.

        На этом уровне:
        - мы ещё не знаем, HTTP это или gRPC,
        - не валидируем данные,
        - просто читаем файл как источник сценария.

        Если файл не найден — это ошибка конфигурации теста,
        а не логики системы, поэтому мы явно падаем.
        """
        mock_file = self.root / file

        if not mock_file.exists():
            self.logger.error(f"Mock file not found: {mock_file}")
            raise FileNotFoundError(f"Mock file not found: {mock_file}")

        self.logger.info(f"Loading mock file: {mock_file}")

        # Используем асинхронное чтение,
        # потому что в будущем этот код будет работать
        # внутри асинхронных mock-серверов.
        async with aiofiles.open(mock_file, mode="r", encoding="utf-8") as async_file:
            return await async_file.read()

    async def load_http(self, file: str, model: Type[HTTPModelT]) -> HTTPModelT:
        """
        Загружает и валидирует HTTP-мок.

        Поток данных:
        JSON-файл -> строка -> Pydantic-модель.

        Таким образом:
        - мы гарантируем соответствие контракта,
        - получаем типизированный объект,
        - избавляемся от работы со словарями в тестах.
        """
        raw = await self.get_raw_data(file)

        self.logger.debug(
            f"Validating HTTP mock with Pydantic model: {model.__name__}"
        )

        return model.model_validate_json(raw)

    async def load_grpc(self, file: str, model: Type[GRPCModelT]) -> GRPCModelT:
        """
        Загружает и валидирует gRPC-мок.

        Поток данных:
        JSON-файл -> строка -> protobuf-сообщение.

        Здесь мы используем стандартный механизм Parse,
        который преобразует JSON в protobuf-объект
        с учётом proto-контракта.
        """
        raw = await self.get_raw_data(file)

        self.logger.debug(
            f"Validating gRPC mock with Protobuf message: {model.__name__}"
        )

        return Parse(raw, model())
