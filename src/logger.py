import logging
from pathlib import Path
from typing import Optional


def setup_logger(name: str, log_file: Optional[str] = None, level: int = logging.DEBUG) -> logging.Logger:
    """
    Настройка логера для модуля.

    :param name: Имя логера (обычно __name__ модуля)
    :param log_file: Имя файла для записи логов (без расширения)
    :param level: Уровень логирования (по умолчанию DEBUG)
    :return: Настроенный логер
    """
    # Создаём папку для логов, если её нет
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    # Создаём логер
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Очищаем существующие обработчики (чтобы избежать дублирования)
    logger.handlers.clear()

    # Создаём обработчик для записи в файл
    if log_file:
        log_path = log_dir / f"{log_file}.log"

        # FileHandler с режимом 'w' для перезаписи при каждом запуске
        file_handler = logging.FileHandler(log_path, mode="w", encoding="utf-8")
        file_handler.setLevel(level)

        # Формат записи лога: метка времени, название модуля, уровень серьезности, сообщение
        file_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
        )
        file_handler.setFormatter(file_formatter)

        # Добавляем обработчик к логеру
        logger.addHandler(file_handler)

    return logger
