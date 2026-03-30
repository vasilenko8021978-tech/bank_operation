from typing import Any

import pytest

from src.processing import filter_by_state, sort_by_date

# ===== ТЕСТЫ ДЛЯ filter_by_state =====


@pytest.mark.parametrize(
    "state, expected_count, description",
    [
        ("EXECUTED", 3, "Должно вернуть 3 выполненные транзакции"),
        ("CANCELED", 2, "Должно вернуть 2 отмененные транзакции"),
    ],
)
def test_filter_by_state_valid(
    transactions_mixed: list[dict], state: str, expected_count: int, description: str
) -> None:
    """Тестирование фильтрации по существующим статусам"""
    result = filter_by_state(transactions_mixed, state)
    assert len(result) == expected_count, description
    assert all(item["state"] == state for item in result)


def test_filter_by_state_default(transactions_mixed: list[dict]) -> None:
    """Тестирование фильтрации со значением по умолчанию (EXECUTED)"""
    result = filter_by_state(transactions_mixed)
    assert len(result) == 3
    assert all(item["state"] == "EXECUTED" for item in result)


def test_filter_by_state_not_found(transactions_no_target_state: list[dict]) -> None:
    """Тестирование фильтрации при отсутствии словарей с указанным статусом"""
    result = filter_by_state(transactions_no_target_state, "EXECUTED")
    assert result == [], "Должен вернуть пустой список, если статус не найден"


def test_filter_by_state_empty_list(empty_list: list) -> None:
    """Тестирование фильтрации пустого списка"""
    result = filter_by_state(empty_list, "EXECUTED")
    assert result == [], "Должен вернуть пустой список для пустого входа"


def test_filter_by_state_single_item(transactions_single: list[dict]) -> None:
    """Тестирование фильтрации списка с одной транзакцией"""
    result = filter_by_state(transactions_single, "EXECUTED")
    assert len(result) == 1
    assert result[0]["id"] == 1


def test_filter_by_state_preserves_original_data(transactions_mixed: list[dict]) -> None:
    """Тестирование, что исходные данные не изменяются"""
    original_ids = [item["id"] for item in transactions_mixed]
    filter_by_state(transactions_mixed, "EXECUTED")
    assert [item["id"] for item in transactions_mixed] == original_ids


@pytest.mark.parametrize(
    "state, expected_result",
    [
        (None, []),
        ("", []),
        (123, []),
        ([], []),
        ({}, []),
    ],
)
def test_filter_by_state_invalid_state_type(transactions_mixed: list[dict], state: Any, expected_result: list) -> None:
    """Тестирование обработки некорректного типа статуса"""
    result = filter_by_state(transactions_mixed, state)
    assert result == expected_result


# ===== ТЕСТЫ ДЛЯ sort_by_date =====


def test_sort_by_date_descending(transactions_unsorted: list[dict]) -> None:
    """Тестирование сортировки по дате в порядке убывания (по умолчанию)"""
    result = sort_by_date(transactions_unsorted)

    # Проверяем, что список отсортирован по убыванию
    dates = [item["date"] for item in result]
    assert dates == sorted(dates, reverse=True), "Даты должны быть отсортированы по убыванию"

    # Проверяем, что первый элемент - самый новый
    assert result[0]["date"] == "2024-01-25T11:00:00"
    assert result[1]["date"] == "2024-01-15T10:00:00"
    assert result[2]["date"] == "2024-01-05T16:45:00"


def test_sort_by_date_ascending(transactions_unsorted: list[dict]) -> None:
    """Тестирование сортировки по дате в порядке возрастания"""
    result = sort_by_date(transactions_unsorted, descending=False)

    # Проверяем, что список отсортирован по возрастанию
    dates = [item["date"] for item in result]
    assert dates == sorted(dates), "Даты должны быть отсортированы по возрастанию"

    # Проверяем, что первый элемент - самый старый
    assert result[0]["date"] == "2024-01-05T16:45:00"
    assert result[1]["date"] == "2024-01-15T10:00:00"
    assert result[2]["date"] == "2024-01-25T11:00:00"


def test_sort_by_date_same_dates(transactions_same_dates: list[dict]) -> None:
    """Тестирование корректности сортировки при одинаковых датах"""
    result = sort_by_date(transactions_same_dates)

    # При одинаковых датах порядок должен сохраниться (стабильная сортировка)
    assert all(item["date"] == "2024-01-15T10:30:00" for item in result)


def test_sort_by_date_single_item(transactions_single: list[dict]) -> None:
    """Тестирование сортировки списка с одной транзакцией"""
    result = sort_by_date(transactions_single)
    assert len(result) == 1
    assert result[0]["id"] == 1


def test_sort_by_date_empty_list(empty_list: list) -> None:
    """Тестирование сортировки пустого списка"""
    result = sort_by_date(empty_list)
    assert result == [], "Должен вернуть пустой список для пустого входа"


@pytest.mark.parametrize(
    "data",
    [
        [{"id": 1, "state": "EXECUTED"}],  # без ключа 'date' - должен вызвать ошибку
    ],
)
def test_sort_by_date_missing_date_key(data: list) -> None:
    """Тестирование обработки отсутствующего ключа 'date'"""
    with pytest.raises(KeyError):
        sort_by_date(data)


def test_sort_by_date_invalid_date_format(transactions_invalid_dates: list[dict]) -> None:
    """Тестирование работы функции с некорректными или нестандартными форматами дат"""
    # Функция использует строковое сравнение, поэтому сортирует лексикографически
    result = sort_by_date(transactions_invalid_dates)

    # Проверяем, что все элементы присутствуют
    assert len(result) == 4

    # При некорректных датах функция возвращает копию исходного списка (без сортировки)
    # Проверяем, что порядок сохранён
    assert result[0]["date"] == "некорректная дата"
    assert result[1]["date"] == "2024-13-01T00:00:00"
    assert result[2]["date"] == "2024-01-40T00:00:00"
    assert result[3]["date"] == "2024/01/15T00:00:00"


@pytest.mark.parametrize(
    "descending, expected_first_date, expected_last_date",
    [
        (True, "2024-01-25T11:00:00", "2024-01-05T16:45:00"),
        (False, "2024-01-05T16:45:00", "2024-01-25T11:00:00"),
    ],
)
def test_sort_by_date_parametrized(
    transactions_unsorted: list[dict], descending: bool, expected_first_date: str, expected_last_date: str
) -> None:
    """Параметризованный тест сортировки"""
    # Исправлено: параметр 'descending' вместо 'reduce'
    result = sort_by_date(transactions_unsorted, descending=descending)

    assert result[0]["date"] == expected_first_date
    assert result[-1]["date"] == expected_last_date
