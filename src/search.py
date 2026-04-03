import re
from typing import Any, Dict, List

from .logger import setup_logger

# Создаём отдельный объект логера для модуля search
logger = setup_logger(__name__, log_file="search")


def search_transactions_by_description(
        transactions: List[Dict[str, Any]],
        search_query: str
) -> List[Dict[str, Any]]:
    """
    Ищет транзакции по описанию с использованием регулярных выражений.

    :param transactions: Список транзакций
    :param search_query: Строка поиска (регулярное выражение)
    :return: Список транзакций, у которых в описании есть искомая строка
    """
    try:
        logger.debug(f"Начат поиск по описанию: '{search_query}'")

        # Компилируем регулярное выражение (игнорируем регистр)
        pattern = re.compile(search_query, re.IGNORECASE)

        results = []
        for transaction in transactions:
            # Ищем ключ "description" с учётом возможных пробелов
            description = ""
            for key, value in transaction.items():
                if isinstance(key, str) and key.strip() == "description":
                    description = str(value).strip()
                    break

            # Проверяем совпадение с регулярным выражением
            if pattern.search(description):
                results.append(transaction)
                logger.debug(f"Найдена транзакция: {description}")

        logger.info(f"Найдено {len(results)} транзакций по запросу '{search_query}'")
        return results

    except re.error as e:
        logger.error(f"Ошибка в регулярном выражении '{search_query}': {e}")
        return []
    except Exception as e:
        logger.error(f"Ошибка при поиске по описанию: {e}", exc_info=True)
        return []


def categorize_transactions(
        transactions: List[Dict[str, Any]],
        categories: List[str]
) -> Dict[str, int]:
    """
    Категоризирует транзакции по заданным категориям на основе описания.

    :param transactions: Список транзакций
    :param categories: Список категорий для поиска в описании
    :return: Словарь {категория: количество операций}
    """
    try:
        logger.debug(f"Начата категоризация по {len(categories)} категориям")

        # Инициализируем словарь с нулевыми значениями
        category_counts = {category: 0 for category in categories}

        for transaction in transactions:
            # Ищем ключ "description" с учётом возможных пробелов
            description = ""
            for key, value in transaction.items():
                if isinstance(key, str) and key.strip() == "description":
                    description = str(value).strip().lower()
                    break

            # Проверяем каждую категорию
            for category in categories:
                # Ищем категорию в описании (игнорируем регистр)
                if category.lower() in description:
                    category_counts[category] += 1
                    logger.debug(f"Транзакция отнесена к категории '{category}': {description}")
                    break  # Одна транзакция относится только к одной категории

        logger.info(f"Категоризация завершена: {category_counts}")
        return category_counts

    except Exception as e:
        logger.error(f"Ошибка при категоризации транзакций: {e}", exc_info=True)
        return {category: 0 for category in categories}

