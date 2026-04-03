import json
import os

import pytest


def clean_transaction_data(data):
    """
    Рекурсивно очищает ВСЕ ключи и строковые значения от пробелов.

    :param data: Данные для очистки (словарь, список или строка)
    :return: Очищенные данные
    """
    if isinstance(data, dict):
        cleaned_dict = {}
        for key, value in data.items():
            # Очищаем ключ (только если это строка)
            cleaned_key = key.strip() if isinstance(key, str) else key
            # Рекурсивно очищаем значение
            cleaned_value = clean_transaction_data(value)
            cleaned_dict[cleaned_key] = cleaned_value
        return cleaned_dict
    elif isinstance(data, list):
        return [clean_transaction_data(item) for item in data]
    elif isinstance(data, str):
        # Очищаем строковые значения
        return data.strip()
    else:
        # Для чисел, булевых значений и т.д. возвращаем как есть
        return data


@pytest.fixture
def sample_transactions():
    """
    Фикстура с реальными данными из файла operations.json.
    ГАРАНТИРОВАННО очищает ВСЕ ключи и значения от пробелов.
    """
    file_path = "data/operations.json"

    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            raw_data = json.load(f)

        # Полная очистка всех данных
        cleaned_data = []
        for transaction in raw_data:
            # Пропускаем пустые объекты (как {} в конце файла)
            if not transaction or not isinstance(transaction, dict):
                continue

            # Очищаем транзакцию
            cleaned_transaction = clean_transaction_data(transaction)
            cleaned_data.append(cleaned_transaction)

        return cleaned_data
    else:
        pytest.skip(f"Файл {file_path} не найден")
        return []


@pytest.fixture
def sample_executed_transactions(sample_transactions):
    """
    Фикстура с выполненными транзакциями (state = "EXECUTED")
    """
    return [tx for tx in sample_transactions if tx.get("state") == "EXECUTED"]


@pytest.fixture
def sample_canceled_transactions(sample_transactions):
    """
    Фикстура с отменёнными транзакциями (state = "CANCELED")
    """
    return [tx for tx in sample_transactions if tx.get("state") == "CANCELED"]


@pytest.fixture
def sample_usd_transactions(sample_transactions):
    """
    Фикстура с транзакциями в валюте USD
    """
    return [tx for tx in sample_transactions if tx.get("operationAmount", {}).get("currency", {}).get("code") == "USD"]


@pytest.fixture
def sample_rub_transactions(sample_transactions):
    """
    Фикстура с транзакциями в валюте RUB
    """
    return [tx for tx in sample_transactions if tx.get("operationAmount", {}).get("currency", {}).get("code") == "RUB"]


@pytest.fixture
def sample_with_from_field(sample_transactions):
    """
    Фикстура с транзакциями, у которых есть поле 'from'
    """
    return [tx for tx in sample_transactions if "from" in tx]


@pytest.fixture
def sample_without_from_field(sample_transactions):
    """
    Фикстура с транзакциями, у которых нет поля 'from'
    """
    return [tx for tx in sample_transactions if "from" not in tx]


@pytest.fixture
def transactions_mixed():
    """Фикстура: смешанные транзакции (3 EXECUTED, 2 CANCELED)"""
    return [
        {"id": 1, "state": "EXECUTED", "date": "2023-01-01T00:00:00"},
        {"id": 2, "state": "EXECUTED", "date": "2023-01-02T00:00:00"},
        {"id": 3, "state": "EXECUTED", "date": "2023-01-03T00:00:00"},
        {"id": 4, "state": "CANCELED", "date": "2023-01-04T00:00:00"},
        {"id": 5, "state": "CANCELED", "date": "2023-01-05T00:00:00"},
    ]


@pytest.fixture
def transactions_no_target_state():
    """Фикстура: транзакции без искомого статуса"""
    return [
        {"id": 1, "state": "CANCELED", "date": "2023-01-01T00:00:00"},
        {"id": 2, "state": "CANCELED", "date": "2023-01-02T00:00:00"},
    ]


@pytest.fixture
def empty_list():
    """Фикстура: пустой список"""
    return []


@pytest.fixture
def transactions_single():
    """Фикстура: одна транзакция"""
    return [{"id": 1, "state": "EXECUTED", "date": "2023-01-01T00:00:00"}]


@pytest.fixture
def transactions_unsorted():
    """Фикстура: неотсортированные транзакции (с датами 2024)"""
    return [
        {"id": 1, "state": "EXECUTED", "date": "2024-01-15T10:00:00"},
        {"id": 2, "state": "EXECUTED", "date": "2024-01-05T16:45:00"},
        {"id": 3, "state": "EXECUTED", "date": "2024-01-25T11:00:00"},
    ]


@pytest.fixture
def transactions_same_dates():
    """Фикстура: транзакции с одинаковыми датами"""
    return [
        {"id": 1, "state": "EXECUTED", "date": "2024-01-15T10:30:00"},
        {"id": 2, "state": "EXECUTED", "date": "2024-01-15T10:30:00"},
        {"id": 3, "state": "EXECUTED", "date": "2024-01-15T10:30:00"},
    ]


@pytest.fixture
def transactions_invalid_dates():
    """Фикстура: транзакции с некорректными датами (4 элемента)"""
    return [
        {"id": 1, "state": "EXECUTED", "date": "некорректная дата"},
        {"id": 2, "state": "EXECUTED", "date": "2024-13-01T00:00:00"},  # Неверный месяц
        {"id": 3, "state": "EXECUTED", "date": "2024-01-40T00:00:00"},  # Неверный день
        {"id": 4, "state": "EXECUTED", "date": "2024/01/15T00:00:00"},  # Неверный формат
    ]
