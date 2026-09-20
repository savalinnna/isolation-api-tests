import logging
from functools import lru_cache


@lru_cache(maxsize=None)
def get_test_logger(name: str) -> logging.Logger:
    """
    Возвращает настроенный логгер для тестового слоя.

    Логгер кэшируется по имени, чтобы:
    - не создавать дубликаты логгеров,
    - избежать повторного добавления хендлеров,
    - сохранить единый формат логирования.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Консольный хендлер используется как базовый способ
    # наблюдения за выполнением тестов и сценариев.
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    # Формат логов выбран так, чтобы по одной строке
    # было понятно, кто логирует, что происходит и когда.
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)

    return logger
