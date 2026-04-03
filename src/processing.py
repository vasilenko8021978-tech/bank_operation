from datetime import datetime
from typing import Any, Dict, Iterator, List


def filter_by_state(transactions: List[Dict[str, Any]], state: str = "EXECUTED") -> List[Dict[str, Any]]:
    """
    Фильтрует транзакции по статусу (state).
    Работает с данными из operations.json (ключи и значения могут содержать пробелы).

    :param transactions: Список транзакций
    :param state: Статус для фильтрации (по умолчанию "EXECUTED")
    :return: Список транзакций с указанным статусом
    """
    if not isinstance(transactions, list) or not isinstance(state, str):
        return []

    filtered = []
    for transaction in transactions:
        if not isinstance(transaction, dict):
            continue

        # Ищем ключ "state" с учётом возможных пробелов
        state_value = None
        for key, value in transaction.items():
            if isinstance(key, str) and key.strip() == "state":
                state_value = value
                break

        if state_value is None:
            continue

        # Очищаем значение статуса от пробелов
        cleaned_state = str(state_value).strip()

        if cleaned_state == state:
            filtered.append(transaction)

    return filtered


def sort_by_date(transactions: List[Dict[str, Any]], descending: bool = True) -> List[Dict[str, Any]]:
    """
    Сортирует транзакции по дате.
    Работает с данными из operations.json (ключи и значения могут содержать пробелы).
    Выбрасывает KeyError, если в транзакции отсутствует ключ 'date'.

    :param transactions: Список транзакций
    :param descending: True для сортировки от новых к старым
    :return: Отсортированный список транзакций
    :raises KeyError: Если в какой-либо транзакции нет ключа 'date'
    """
    if not isinstance(transactions, list):
        return []

    # Проверяем наличие ключа 'date' во всех транзакциях
    for tx in transactions:
        if not isinstance(tx, dict):
            continue

        date_found = False
        for key in tx.keys():
            if isinstance(key, str) and key.strip() == "date":
                date_found = True
                break

        if not date_found:
            raise KeyError("Отсутствует ключ 'date' в транзакции")

    # Сортируем по дате
    try:
        sorted_transactions = []
        for tx in transactions:
            if not isinstance(tx, dict):
                continue

            # Ищем и извлекаем дату
            date_value = None
            for key, value in tx.items():
                if isinstance(key, str) and key.strip() == "date":
                    date_value = value
                    break

            if date_value is None:
                continue

            # Очищаем значение даты от пробелов
            cleaned_date = str(date_value).strip()
            sorted_transactions.append((cleaned_date, tx))

        sorted_transactions.sort(key=lambda x: datetime.fromisoformat(x[0]), reverse=descending)

        # Возвращаем только транзакции (без дат)
        return [tx for _, tx in sorted_transactions]
    except (ValueError, TypeError):
        # При ошибке парсинга возвращаем исходный список
        return transactions.copy()


def transaction_descriptions(transactions: List[Dict[str, Any]]) -> Iterator[str]:
    """
    Генератор описаний транзакций.
    Работает с данными из operations.json (ключи и значения могут содержать пробелы).

    :param transactions: Список транзакций
    :return: Итератор строк с описаниями
    """
    for tx in transactions:
        if not isinstance(tx, dict):
            continue

        # Ищем ключ "description" с учётом возможных пробелов
        description = "Без описания"
        for key, value in tx.items():
            if isinstance(key, str) and key.strip() == "description":
                description = str(value).strip() if value else "Без описания"
                break

        yield description
