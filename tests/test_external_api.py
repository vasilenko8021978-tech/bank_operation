import pytest
import json
import os


@pytest.fixture
def sample_transactions():
    """
    Фикстура с реальными данными из файла operations.json.
    Автоматически очищает ВСЕ ключи и значения от пробелов.
    """
    file_path = "data/operations.json"

    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Рекурсивная функция для очистки ключей и значений
        def clean_data_recursive(data):
            if isinstance(data, dict):
                return {k.strip() if isinstance(k, str) else k: clean_data_recursive(v) for k, v in data.items()}
            elif isinstance(data, list):
                return [clean_data_recursive(item) for item in data]
            elif isinstance(data, str):
                return data.strip()
            else:
                return data

        # Очистка всех данных
        cleaned_data = []
        for transaction in data:  # ← Исправлено: добавлено "data"
            if not transaction:  # Пропускаем пустые транзакции
                continue
            cleaned_data.append(clean_data_recursive(transaction))

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
    return [
        tx
        for tx in sample_transactions
        if tx.get("operationAmount", {}).get("currency", {}).get("code", "").strip() == "USD"
    ]


@pytest.fixture
def sample_rub_transactions(sample_transactions):
    """
    Фикстура с транзакциями в валюте RUB
    """
    return [
        tx
        for tx in sample_transactions
        if tx.get("operationAmount", {}).get("currency", {}).get("code", "").strip() == "RUB"
    ]


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
def sample_transaction_usd():
    """Фикстура: транзакция в USD из operations.json"""
    return {
        "id ": 41428829,
        "state ": "EXECUTED ",
        "date ": "2019-07-03T18:35:29.512364 ",
        "operationAmount ": {"amount ": "8221.37 ", "currency ": {"name ": "USD ", "code ": "USD "}},
        "description ": "Перевод организации ",
        "from ": "MasterCard 7158300734726758 ",
        "to ": "Счет 35383033474447895560 ",
    }


@pytest.fixture
def sample_transaction_rub():
    """Фикстура: транзакция в RUB из operations.json"""
    return {
        "id ": 441945886,
        "state ": "EXECUTED ",
        "date ": "2019-08-26T10:50:58.294041 ",
        "operationAmount ": {"amount ": "31957.58 ", "currency ": {"name ": "руб. ", "code ": "RUB "}},
        "description ": "Перевод организации ",
        "from ": "Maestro 1596837868705199 ",
        "to ": "Счет 64686473678894779589 ",
    }
