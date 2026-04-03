import json
import os
from unittest.mock import mock_open, patch

import pytest

from src.utils import read_transactions_from_json

# ===== ТЕСТЫ С ИСПОЛЬЗОВАНИЕМ MOCK И PATCH =====


@patch("src.utils.os.path.exists")
@patch("src.utils.open", new_callable=mock_open, read_data='[{"id": 1, "amount": "100.00"}]')
@patch("src.utils.json.loads")
def test_read_transactions_from_json_valid_file(mock_json_loads, mock_open_file, mock_exists):
    """Тестирование чтения валидного JSON-файла с использованием моков"""
    # Настройка моков
    mock_exists.return_value = True
    mock_json_loads.return_value = [{"id": 1, "amount": "100.00"}]

    # Вызов функции
    result = read_transactions_from_json("test.json")

    # Проверки
    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0]["id"] == 1
    assert result[0]["amount"] == "100.00"

    # Проверка вызовов моков
    mock_exists.assert_called_once_with("test.json")
    mock_open_file.assert_called_once_with("test.json", "r", encoding="utf-8")
    mock_json_loads.assert_called_once()


@patch("src.utils.os.path.exists")
def test_read_transactions_from_json_nonexistent_file(mock_exists):
    """Тестирование чтения несуществующего файла"""
    # Настройка мока
    mock_exists.return_value = False

    # Вызов функции
    result = read_transactions_from_json("nonexistent.json")

    # Проверки
    assert result == []
    mock_exists.assert_called_once_with("nonexistent.json")


@patch("src.utils.os.path.exists")
@patch("src.utils.open", new_callable=mock_open, read_data="")
def test_read_transactions_from_json_empty_file(mock_open_file, mock_exists):
    """Тестирование чтения пустого файла"""
    # Настройка моков
    mock_exists.return_value = True

    # Вызов функции
    result = read_transactions_from_json("empty.json")

    # Проверки
    assert result == []
    mock_exists.assert_called_once_with("empty.json")
    mock_open_file.assert_called_once_with("empty.json", "r", encoding="utf-8")


@patch("src.utils.os.path.exists")
@patch("src.utils.open", new_callable=mock_open, read_data="{invalid json}")
@patch("src.utils.json.loads")
def test_read_transactions_from_json_invalid_json(mock_json_loads, mock_open_file, mock_exists):
    """Тестирование чтения невалидного JSON"""
    # Настройка моков
    mock_exists.return_value = True
    mock_json_loads.side_effect = json.JSONDecodeError("Expecting value", "{invalid json}", 0)

    # Вызов функции
    result = read_transactions_from_json("invalid.json")

    # Проверки
    assert result == []
    mock_exists.assert_called_once_with("invalid.json")
    mock_json_loads.assert_called_once()


@patch("src.utils.os.path.exists")
@patch("src.utils.open", new_callable=mock_open, read_data='{"not": "a list"}')
@patch("src.utils.json.loads")
def test_read_transactions_from_json_non_list_content(mock_json_loads, mock_open_file, mock_exists):
    """Тестирование чтения файла, содержащего не список"""
    # Настройка моков
    mock_exists.return_value = True
    mock_json_loads.return_value = {"not": "a list"}

    # Вызов функции
    result = read_transactions_from_json("non_list.json")

    # Проверки
    assert result == []
    mock_exists.assert_called_once_with("non_list.json")
    mock_json_loads.assert_called_once()


@patch("src.utils.os.path.exists")
@patch("src.utils.open", new_callable=mock_open, read_data='[{"id ": 1, "amount ": "100.00 "}]')
@patch("src.utils.json.loads")
def test_read_transactions_from_json_with_spaces_in_keys(mock_json_loads, mock_open_file, mock_exists):
    """Тестирование очистки ключей и значений от пробелов (как в operations.json)"""
    # Настройка моков
    mock_exists.return_value = True
    # Имитируем данные как в operations.json (с пробелами в ключах и значениях)
    mock_json_loads.return_value = [{"id ": 1, "amount ": "100.00 "}]

    # Вызов функции
    result = read_transactions_from_json("operations.json")

    # Проверки
    assert isinstance(result, list)
    assert len(result) == 1

    # Ключи и значения должны быть очищены от пробелов
    transaction = result[0]
    assert "id" in transaction  # Ключ без пробела
    assert transaction["id"] == 1
    assert "amount" in transaction  # Ключ без пробела
    assert transaction["amount"] == "100.00"  # Значение без пробела

    mock_exists.assert_called_once_with("operations.json")
    mock_json_loads.assert_called_once()


@patch("src.utils.os.path.exists")
@patch("src.utils.open")
@patch("src.utils.json.loads")
def test_read_transactions_from_json_io_error(mock_json_loads, mock_open_file, mock_exists):
    """Тестирование обработки ошибки ввода-вывода"""
    # Настройка моков
    mock_exists.return_value = True
    mock_open_file.side_effect = IOError("Permission denied")

    # Вызов функции
    result = read_transactions_from_json("protected.json")

    # Проверки
    assert result == []
    mock_exists.assert_called_once_with("protected.json")


# ===== ТЕСТЫ С РЕАЛЬНЫМИ ДАННЫМИ ИЗ ОПЕРАЦИЙ =====


def test_read_transactions_from_json_real_file(sample_transactions):
    """
    Тестирование чтения реального файла operations.json через фикстуру.
    Фикстура уже обрабатывает очистку ключей от пробелов.
    """
    # Проверяем, что фикстура возвращает список
    assert isinstance(sample_transactions, list)

    # Проверяем, что список не пустой
    assert len(sample_transactions) > 0

    # Проверяем структуру первой транзакции
    first_tx = sample_transactions[0]
    assert "id" in first_tx
    assert "state" in first_tx
    assert "date" in first_tx
    assert "operationAmount" in first_tx
    assert "description" in first_tx

    # Проверяем, что ключи очищены от пробелов
    assert "id " not in first_tx  # Нет ключа с пробелом
    assert "state " not in first_tx  # Нет ключа с пробелом


def test_read_transactions_from_json_executed_count(sample_executed_transactions):
    """Тестирование количества выполненных транзакций"""
    # Проверяем, что фикстура возвращает список
    assert isinstance(sample_executed_transactions, list)

    # Проверяем, что есть хотя бы одна выполненная транзакция
    assert len(sample_executed_transactions) > 0

    # Проверяем, что все транзакции имеют статус EXECUTED
    for tx in sample_executed_transactions:
        assert tx.get("state") == "EXECUTED"


def test_read_transactions_from_json_canceled_count(sample_canceled_transactions):
    """Тестирование количества отменённых транзакций"""
    # Проверяем, что фикстура возвращает список
    assert isinstance(sample_canceled_transactions, list)

    # Проверяем, что есть хотя бы одна отменённая транзакция
    assert len(sample_canceled_transactions) > 0

    # Проверяем, что все транзакции имеют статус CANCELED
    for tx in sample_canceled_transactions:
        assert tx.get("state") == "CANCELED"


def test_read_transactions_from_json_usd_currency(sample_usd_transactions):
    """Тестирование транзакций в валюте USD"""
    # Проверяем, что фикстура возвращает список
    assert isinstance(sample_usd_transactions, list)

    # Проверяем, что есть хотя бы одна транзакция в USD
    assert len(sample_usd_transactions) > 0

    # Проверяем, что все транзакции действительно в USD
    for tx in sample_usd_transactions:
        currency_code = tx.get("operationAmount", {}).get("currency", {}).get("code", "").strip()
        assert currency_code == "USD"


def test_read_transactions_from_json_rub_currency(sample_rub_transactions):
    """Тестирование транзакций в валюте RUB"""
    # Проверяем, что фикстура возвращает список
    assert isinstance(sample_rub_transactions, list)

    # Проверяем, что есть хотя бы одна транзакция в RUB
    assert len(sample_rub_transactions) > 0

    # Проверяем, что все транзакции действительно в RUB
    for tx in sample_rub_transactions:
        currency_code = tx.get("operationAmount", {}).get("currency", {}).get("code", "").strip()
        assert currency_code == "RUB"


def test_read_transactions_from_json_with_from_field(sample_with_from_field):
    """Тестирование транзакций с полем 'from'"""
    # Проверяем, что фикстура возвращает список
    assert isinstance(sample_with_from_field, list)

    # Проверяем, что есть хотя бы одна транзакция с полем 'from'
    assert len(sample_with_from_field) > 0

    # Проверяем, что у всех этих транзакций есть поле 'from'
    for tx in sample_with_from_field:
        assert "from" in tx


def test_read_transactions_from_json_without_from_field(sample_without_from_field):
    """Тестирование транзакций без поля 'from'"""
    # Проверяем, что фикстура возвращает список
    assert isinstance(sample_without_from_field, list)

    # Проверяем, что есть хотя бы одна транзакция без поля 'from'
    assert len(sample_without_from_field) > 0

    # Проверяем, что у всех этих транзакций нет поля 'from'
    for tx in sample_without_from_field:
        assert "from" not in tx


# ===== ИНТЕГРАЦИОННЫЕ ТЕСТЫ =====


@pytest.mark.skipif(not os.path.exists("data/operations.json"), reason="Файл operations.json не найден")
def test_integration_read_real_operations_file():
    """Интеграционный тест: чтение реального файла operations.json"""
    # Чтение данных из реального файла
    transactions = read_transactions_from_json("data/operations.json")

    # Проверки
    assert isinstance(transactions, list)
    assert len(transactions) > 0

    # Проверяем первую транзакцию
    first_tx = transactions[0]
    assert "id" in first_tx
    assert "state" in first_tx
    assert "date" in first_tx
    assert "operationAmount" in first_tx
    assert "description" in first_tx

    # Проверяем структуру operationAmount
    assert "amount" in first_tx["operationAmount"]
    assert "currency" in first_tx["operationAmount"]

    # Проверяем структуру currency
    assert "name" in first_tx["operationAmount"]["currency"]
    assert "code" in first_tx["operationAmount"]["currency"]

    # Проверяем, что ключи очищены от пробелов
    assert "id " not in first_tx
    assert "state " not in first_tx


@pytest.mark.skipif(not os.path.exists("data/operations.json"), reason="Файл operations.json не найден")
def test_integration_filter_usd_transactions():
    """Интеграционный тест: фильтрация транзакций в USD после чтения"""
    from src.generators import filter_by_currency

    # Чтение данных
    transactions = read_transactions_from_json("data/operations.json")

    # Фильтрация транзакций в USD
    usd_transactions = list(filter_by_currency(transactions, "USD"))

    # Проверки
    assert len(usd_transactions) > 0

    # Проверяем, что все транзакции в USD
    for tx in usd_transactions:
        currency_code = tx["operationAmount"]["currency"]["code"].strip()
        assert currency_code == "USD"


@pytest.mark.skipif(not os.path.exists("data/operations.json"), reason="Файл operations.json не найден")
def test_integration_get_transaction_descriptions():
    """Интеграционный тест: получение описаний транзакций после чтения"""
    from src.generators import transaction_description

    # Чтение данных
    transactions = read_transactions_from_json("data/operations.json")

    # Получение описаний
    descriptions = list(transaction_description(transactions))

    # Проверки
    assert len(descriptions) == len(transactions)

    # Проверяем, что все описания не пустые
    for desc in descriptions:
        assert desc is not None
        assert isinstance(desc, str)


# ===== ТЕСТЫ ГРАНИЧНЫХ СЛУЧАЕВ =====


@patch("src.utils.os.path.exists")
@patch("src.utils.open", new_callable=mock_open, read_data='[{"id": 1}, {"id": 2}, {"id": 3}]')
@patch("src.utils.json.loads")
def test_read_transactions_from_json_large_file(mock_json_loads, mock_open_file, mock_exists):
    """Тестирование чтения большого файла (1000+ транзакций)"""
    # Настройка моков
    mock_exists.return_value = True
    mock_json_loads.return_value = [{"id": i} for i in range(1000)]

    # Вызов функции
    result = read_transactions_from_json("large_file.json")

    # Проверки
    assert isinstance(result, list)
    assert len(result) == 1000
    assert result[0]["id"] == 0
    assert result[999]["id"] == 999


@patch("src.utils.os.path.exists")
@patch("src.utils.open", new_callable=mock_open, read_data='[{"id": 1, "description": "Платёж за товар №123"}]')
@patch("src.utils.json.loads")
def test_read_transactions_from_json_special_characters(mock_json_loads, mock_open_file, mock_exists):
    """Тестирование чтения файла со специальными символами"""
    # Настройка моков
    mock_exists.return_value = True
    mock_json_loads.return_value = [{"id": 1, "description": "Платёж за товар №123"}]

    # Вызов функции
    result = read_transactions_from_json("special_chars.json")

    # Проверки
    assert len(result) == 1
    assert result[0]["description"] == "Платёж за товар №123"


@patch("src.utils.os.path.exists")
@patch("src.utils.open", new_callable=mock_open, read_data="[]")
@patch("src.utils.json.loads")
def test_read_transactions_from_json_empty_list(mock_json_loads, mock_open_file, mock_exists):
    """Тестирование чтения файла с пустым списком"""
    # Настройка моков
    mock_exists.return_value = True
    mock_json_loads.return_value = []

    # Вызов функции
    result = read_transactions_from_json("empty_list.json")

    # Проверки
    assert result == []
    assert isinstance(result, list)
