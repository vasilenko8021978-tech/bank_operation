import pytest

# Фикстуры для filter_by_state


@pytest.fixture
def transactions_mixed() -> list[dict]:
    """Список транзакций с разными статусами"""
    return [
        {"id": 1, "state": "EXECUTED", "date": "2024-01-15T10:30:00"},
        {"id": 2, "state": "CANCELED", "date": "2024-01-14T09:15:00"},
        {"id": 3, "state": "EXECUTED", "date": "2024-01-13T14:20:00"},
        {"id": 4, "state": "EXECUTED", "date": "2024-01-11T11:00:00"},
        {"id": 5, "state": "CANCELED", "date": "2024-01-10T08:30:00"},
    ]


@pytest.fixture
def empty_list() -> list:
    """Пустой список"""
    return []


@pytest.fixture
def transactions_no_target_state() -> list[dict]:
    """Список без транзакций с определённым статусом"""
    return [
        {"id": 1, "state": "CANCELED", "date": "2024-01-01T00:00:00"},
        {"id": 3, "state": "CANCELED", "date": "2024-01-03T00:00:00"},
    ]


@pytest.fixture
def transactions_single() -> list[dict]:
    """Список с одной транзакцией"""
    return [{"id": 1, "state": "EXECUTED", "date": "2024-01-01T00:00:00"}]


# Фикстуры для sort_by_date


@pytest.fixture
def transactions_unsorted() -> list[dict]:
    """Список транзакций с неотсортированными датами"""
    return [
        {"id": 1, "state": "EXECUTED", "date": "2024-01-15T10:30:00"},
        {"id": 2, "state": "CANCELED", "date": "2024-01-10T09:15:00"},
        {"id": 3, "state": "EXECUTED", "date": "2024-01-20T14:20:00"},
        {"id": 4, "state": "PENDING", "date": "2024-01-05T16:45:00"},
        {"id": 5, "state": "EXECUTED", "date": "2024-01-25T11:00:00"},
    ]


@pytest.fixture
def transactions_same_dates() -> list[dict]:
    """Список транзакций с одинаковыми датами"""
    return [
        {"id": 1, "state": "EXECUTED", "date": "2024-01-15T10:30:00"},
        {"id": 2, "state": "CANCELED", "date": "2024-01-15T10:30:00"},
        {"id": 3, "state": "EXECUTED", "date": "2024-01-15T10:30:00"},
    ]


@pytest.fixture
def transactions_invalid_dates() -> list[dict]:
    """Список транзакций с некорректными форматами дат"""
    return [
        {"id": 1, "state": "EXECUTED", "date": "2024-01-15"},  # без времени
        {"id": 2, "state": "CANCELED", "date": "15.01.2024"},  # другой формат
        {"id": 3, "state": "EXECUTED", "date": "invalid_date"},  # невалидная дата
        {"id": 4, "state": "CANCELED", "date": "2024/01/15"},  # другой разделитель
    ]


@pytest.fixture
def transactions_missing_date() -> list[dict]:
    """Список транзакций без ключа 'date'"""
    return [
        {"id": 1, "state": "EXECUTED"},  # нет ключа 'date'
        {"id": 2, "state": "CANCELED", "date": "2024-01-15T10:30:00"},
    ]
