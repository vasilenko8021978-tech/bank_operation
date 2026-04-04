import re
from typing import List, Dict, Any
from collections import Counter  # ← Добавлен импорт Counter
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
    Использует Counter для эффективного подсчёта.

    :param transactions: Список транзакций
    :param categories: Список категорий для поиска в описании
    :return: Словарь {категория: количество операций}
    """
    try:
        logger.debug(f"Начата категоризация по {len(categories)} категориям")

        # Список найденных категорий для каждой транзакции
        found_categories: List[str] = []

        for transaction in transactions:
            # Ищем ключ "description" с учётом возможных пробелов
            description = ""
            for key, value in transaction.items():
                if isinstance(key, str) and key.strip() == "description":
                    description = str(value).strip().lower()
                    break

            # Проверяем каждую категорию (в порядке списка)
            for category in categories:
                # Ищем категорию в описании (игнорируем регистр)
                if category.lower() in description:
                    found_categories.append(category)
                    logger.debug(f"Транзакция отнесена к категории '{category}': {description}")
                    break  # Одна транзакция относится только к одной категории

        # Используем Counter для подсчёта категорий
        category_counter = Counter(found_categories)

        # Формируем результат: все категории из исходного списка с их количеством (0 если нет)
        result = {category: category_counter.get(category, 0) for category in categories}

        logger.info(f"Категоризация завершена: {result}")
        return result

    except Exception as e:
        logger.error(f"Ошибка при категоризации транзакций: {e}", exc_info=True)
        return {category: 0 for category in categories}

