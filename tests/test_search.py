import pytest

from src.search import categorize_transactions, search_transactions_by_description


@pytest.fixture
def sample_transactions():
    """Фикстура с тестовыми транзакциями"""
    return [
        {
            "id": 1,
            "state": "EXECUTED",
            "date": "2019-08-26T10:50:58.294041",
            "operationAmount": {
                "amount": "31957.58",
                "currency": {"name": "руб.", "code": "RUB"}
            },
            "description": "Перевод организации",
            "from": "Maestro 1596837868705199",
            "to": "Счет 64686473678894779589"
        },
        {
            "id": 2,
            "state": "EXECUTED",
            "date": "2019-07-03T18:35:29.512364",
            "operationAmount": {
                "amount": "8221.37",
                "currency": {"name": "USD", "code": "USD"}
            },
            "description": "Перевод с карты на карту",
            "from": "MasterCard 7158300734726758",
            "to": "Счет 35383033474447895560"
        },
        {
            "id": 3,
            "state": "EXECUTED",
            "date": "2018-03-23T10:45:06.972075",
            "operationAmount": {
                "amount": "48223.05",
                "currency": {"name": "руб.", "code": "RUB"}
            },
            "description": "Открытие вклада",
            "to": "Счет 41421565395219882431"
        },
        {
            "id": 4,
            "state": "CANCELED",
            "date": "2018-09-12T21:27:25.241689",
            "operationAmount": {
                "amount": "67314.70",
                "currency": {"name": "руб.", "code": "RUB"}
            },
            "description": "Перевод организации",
            "from": "Visa Platinum 1246377376343588",
            "to": "Счет 14211924144426031657"
        }
    ]


def test_search_transactions_by_description_simple(sample_transactions):
    """Тестирование простого поиска по описанию"""
    # Поиск по слову "организации"
    result = search_transactions_by_description(sample_transactions, "организации")
    assert len(result) == 2
    assert result[0]["id"] == 1
    assert result[1]["id"] == 4


def test_search_transactions_by_description_case_insensitive(sample_transactions):
    """Тестирование поиска без учёта регистра"""
    # Поиск в разном регистре
    result1 = search_transactions_by_description(sample_transactions, "перевод")
    result2 = search_transactions_by_description(sample_transactions, "ПЕРЕВОД")
    result3 = search_transactions_by_description(sample_transactions, "Перевод")

    assert len(result1) == 3
    assert len(result2) == 3
    assert len(result3) == 3


def test_search_transactions_by_description_regex(sample_transactions):
    """Тестирование поиска с регулярным выражением"""
    # Поиск по шаблону (слова, начинающиеся на "откр")
    result = search_transactions_by_description(sample_transactions, r"откр\w+")
    assert len(result) == 1
    assert result[0]["description"] == "Открытие вклада"


def test_search_transactions_by_description_no_match(sample_transactions):
    """Тестирование поиска без совпадений"""
    result = search_transactions_by_description(sample_transactions, "несуществующее_слово")
    assert len(result) == 0


def test_search_transactions_by_description_invalid_regex(sample_transactions):
    """Тестирование обработки невалидного регулярного выражения"""
    # Невалидное регулярное выражение
    result = search_transactions_by_description(sample_transactions, "[")
    assert len(result) == 0  # Должен вернуть пустой список без ошибки


def test_categorize_transactions_basic(sample_transactions):
    """Тестирование базовой категоризации"""
    categories = ["Перевод организации", "Открытие вклада", "Перевод с карты на карту"]
    result = categorize_transactions(sample_transactions, categories)

    assert result["Перевод организации"] == 2
    assert result["Открытие вклада"] == 1
    assert result["Перевод с карты на карту"] == 1


def test_categorize_transactions_case_insensitive(sample_transactions):
    """Тестирование категоризации без учёта регистра"""
    categories = ["перевод организации", "открытие вклада"]
    result = categorize_transactions(sample_transactions, categories)

    # Должно найти совпадения несмотря на разный регистр
    assert result["перевод организации"] == 2
    assert result["открытие вклада"] == 1


def test_categorize_transactions_empty_categories(sample_transactions):
    """Тестирование категоризации с пустым списком категорий"""
    result = categorize_transactions(sample_transactions, [])
    assert result == {}


def test_categorize_transactions_no_matches(sample_transactions):
    """Тестирование категоризации без совпадений"""
    categories = ["несуществующая категория"]
    result = categorize_transactions(sample_transactions, categories)
    assert result["несуществующая категория"] == 0
