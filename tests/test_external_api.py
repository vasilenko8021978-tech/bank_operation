import pytest
import os
from unittest.mock import patch
from src.external_api import (
    get_exchange_rate,
    get_transaction_amount_in_rubles,
    ExchangeRateError
)


@pytest.fixture
def mock_env_vars() -> None:
    """Фикстура для мокирования переменных окружения"""
    with patch.dict(os.environ, {"EXCHANGE_RATES_API_KEY": "test_api_key_123"}):
        yield


@pytest.fixture
def sample_transaction_usd() -> dict:
    """Фикстура: транзакция в USD из operations.json"""
    return {
        "id ": 41428829,
        "state ": "EXECUTED ",
        "date ": "2019-07-03T18:35:29.512364 ",
        "operationAmount ": {
            "amount ": "8221.37 ",
            "currency ": {
                "name ": "USD ",
                "code ": "USD "
            }
        },
        "description ": "Перевод организации ",
        "from ": "MasterCard 7158300734726758 ",
        "to ": "Счет 35383033474447895560 "
    }


@pytest.fixture
def sample_transaction_rub() -> dict:
    """Фикстура: транзакция в RUB из operations.json"""
    return {
        "id ": 441945886,
        "state ": "EXECUTED ",
        "date ": "2019-08-26T10:50:58.294041 ",
        "operationAmount ": {
            "amount ": "31957.58 ",
            "currency ": {
                "name ": "руб. ",
                "code ": "RUB "
            }
        },
        "description ": "Перевод организации ",
        "from ": "Maestro 1596837868705199 ",
        "to ": "Счет 64686473678894779589 "
    }


@patch("src.external_api.requests.get")
def test_get_exchange_rate_success(mock_get, mock_env_vars) -> None:
    """Тестирование успешного получения курса валют"""
    # Настройка мока
    mock_response = type("MockResponse", (), {
        "json": lambda self: {
            "success": True,
            "timestamp": 1678901234,
            "base": "USD",
            "date": "2023-03-15",
            "rates": {"RUB": 92.45}
        },
        "raise_for_status": lambda self: None
    })()
    mock_get.return_value = mock_response

    # Вызов функции
    rate: float = get_exchange_rate("USD", "RUB")

    # Проверки
    assert rate == 92.45
    mock_get.assert_called_once()


@patch("src.external_api.requests.get")
def test_get_exchange_rate_api_error(mock_get, mock_env_vars) -> None:
    """Тестирование обработки ошибки API"""
    # Настройка мока
    mock_response = type("MockResponse", (), {
        "json": lambda self: {
            "success": False,
            "error": {
                "info": "Invalid API key"
            }
        },
        "raise_for_status": lambda self: None
    })()
    mock_get.return_value = mock_response

    # Вызов функции и проверка исключения
    with pytest.raises(ExchangeRateError, match="Ошибка API: Invalid API key"):
        get_exchange_rate("USD", "RUB")


@patch("src.external_api.requests.get")
def test_get_exchange_rate_network_error(mock_get, mock_env_vars) -> None:
    """Тестирование обработки сетевой ошибки"""
    # Настройка мока
    from requests.exceptions import RequestException
    mock_get.side_effect = RequestException("Connection error")

    # Вызов функции и проверка исключения
    with pytest.raises(ExchangeRateError, match="Ошибка сети при запросе к API"):
        get_exchange_rate("USD", "RUB")


@patch("src.external_api.requests.get")
def test_get_exchange_rate_timeout(mock_get, mock_env_vars) -> None:
    """Тестирование обработки таймаута"""
    # Настройка мока
    from requests.exceptions import Timeout
    mock_get.side_effect = Timeout("Request timed out")

    # Вызов функции и проверка исключения
    with pytest.raises(ExchangeRateError, match="Таймаут запроса к API"):
        get_exchange_rate("USD", "RUB")


def test_get_exchange_rate_missing_api_key() -> None:
    """Тестирование отсутствия API ключа"""
    # Убеждаемся, что переменная окружения не установлена
    with patch.dict(os.environ, {}, clear=True):
        with pytest.raises(ExchangeRateError, match="API ключ не найден"):
            get_exchange_rate("USD", "RUB")


@patch("src.external_api.convert_amount_to_rubles")
def test_get_transaction_amount_in_rubles_usd(mock_convert, sample_transaction_usd) -> None:
    """Тестирование получения суммы транзакции в рублях (USD)"""
    # Настройка мока
    mock_convert.return_value = 75900.57

    # Вызов функции
    result: float = get_transaction_amount_in_rubles(sample_transaction_usd)

    # Проверки
    assert result == 75900.57
    mock_convert.assert_called_once()
    call_args = mock_convert.call_args[0]
    assert call_args[0] == "8221.37"  # Сумма без пробелов
    assert call_args[1] == "USD"  # Код валюты без пробелов


@patch("src.external_api.convert_amount_to_rubles")
def test_get_transaction_amount_in_rubles_rub(mock_convert, sample_transaction_rub) -> None:
    """Тестирование получения суммы транзакции в рублях (RUB)"""
    # Настройка мока
    mock_convert.return_value = 31957.58

    # Вызов функции
    result: float = get_transaction_amount_in_rubles(sample_transaction_rub)

    # Проверки
    assert result == 31957.58
    mock_convert.assert_called_once()
    call_args = mock_convert.call_args[0]
    assert call_args[0] == "31957.58"
    assert call_args[1] == "RUB"


@patch("src.external_api.convert_amount_to_rubles")
def test_get_transaction_amount_in_rubles_operationAmount_not_dict(mock_convert) -> None:
    """Тестирование обработки случая, когда operationAmount не является словарём"""
    # Транзакция с operationAmount в виде строки (невалидный тип)
    invalid_transaction = {
        "operationAmount": "invalid_string_instead_of_dict"
    }

    with pytest.raises(ValueError,
                       match="Ошибка при обработке транзакции: Поле 'operationAmount' должно быть словарём"):
        get_transaction_amount_in_rubles(invalid_transaction)


@patch("src.external_api.convert_amount_to_rubles")
def test_get_transaction_amount_in_rubles_missing_operationAmount(mock_convert) -> None:
    """Тестирование обработки транзакции без поля operationAmount"""
    # Транзакция без operationAmount
    invalid_transaction = {"id": 1, "description": "Test"}

    with pytest.raises(ValueError, match="Ошибка при обработке транзакции: Сумма транзакции не указана"):
        get_transaction_amount_in_rubles(invalid_transaction)


@patch("src.external_api.convert_amount_to_rubles")
def test_get_transaction_amount_in_rubles_missing_amount(mock_convert) -> None:
    """Тестирование обработки транзакции без суммы"""
    # Транзакция без суммы в operationAmount
    invalid_transaction = {
        "operationAmount": {
            "currency": {"code": "USD"}
        }
    }

    with pytest.raises(ValueError, match="Ошибка при обработке транзакции: Сумма транзакции не указана"):
        get_transaction_amount_in_rubles(invalid_transaction)


@patch("src.external_api.convert_amount_to_rubles")
def test_get_transaction_amount_in_rubles_missing_currency_code(mock_convert) -> None:
    """Тестирование обработки транзакции без кода валюты"""
    # Транзакция без кода валюты
    invalid_transaction = {
        "operationAmount": {
            "amount": "100.00",
            "currency": {"name": "USD"}
        }
    }

    with pytest.raises(ValueError, match="Ошибка при обработке транзакции: Код валюты не указан"):
        get_transaction_amount_in_rubles(invalid_transaction)


@patch("src.external_api.convert_amount_to_rubles")
def test_get_transaction_amount_in_rubles_with_spaces_in_keys(mock_convert, sample_transaction_usd) -> None:
    """Тестирование обработки ключей с пробелами (как в operations.json)"""
    # Транзакция уже содержит пробелы в ключах (см. фикстуру)
    mock_convert.return_value = 75900.57

    result = get_transaction_amount_in_rubles(sample_transaction_usd)

    # Должно корректно обработать ключи с пробелами
    assert result == 75900.57
    mock_convert.assert_called_once_with("8221.37", "USD")


@patch("src.external_api.get_exchange_rate")
def test_convert_amount_to_rubles_rub(mock_get_rate) -> None:
    """Тестирование конвертации суммы в рублях (без конвертации)"""
    # Вызов функции
    from src.external_api import convert_amount_to_rubles
    result = convert_amount_to_rubles(1000.50, "RUB")

    # Проверки
    assert result == 1000.50
    assert isinstance(result, float)
    mock_get_rate.assert_not_called()  # Курс не запрашивается для RUB


@patch("src.external_api.get_exchange_rate")
def test_convert_amount_to_rubles_usd(mock_get_rate) -> None:
    """Тестирование конвертации суммы из USD в рубли"""
    # Настройка мока
    mock_get_rate.return_value = 92.45

    # Вызов функции
    from src.external_api import convert_amount_to_rubles
    result = convert_amount_to_rubles(100.00, "USD")

    # Проверки
    assert result == 9245.00  # 100 * 92.45 = 9245.00
    assert isinstance(result, float)
    mock_get_rate.assert_called_once_with("USD", "RUB")


@patch("src.external_api.get_exchange_rate")
def test_convert_amount_to_rubles_eur(mock_get_rate) -> None:
    """Тестирование конвертации суммы из EUR в рубли"""
    # Настройка мока
    mock_get_rate.return_value = 101.20

    # Вызов функции
    from src.external_api import convert_amount_to_rubles
    result = convert_amount_to_rubles(50.00, "EUR")

    # Проверки
    assert result == 5060.00  # 50 * 101.20 = 5060.00
    mock_get_rate.assert_called_once_with("EUR", "RUB")


@patch("src.external_api.get_exchange_rate")
def test_convert_amount_to_rubles_rounding(mock_get_rate) -> None:
    """Тестирование округления результата до 2 знаков"""
    # Настройка мока с "плохим" числом
    mock_get_rate.return_value = 92.456789

    # Вызов функции
    from src.external_api import convert_amount_to_rubles
    result = convert_amount_to_rubles(1.00, "USD")

    # Проверки (должно округлиться до 92.46)
    assert result == 92.46
    assert isinstance(result, float)


def test_convert_amount_to_rubles_unsupported_currency() -> None:
    """Тестирование конвертации неподдерживаемой валюты"""
    from src.external_api import convert_amount_to_rubles

    with pytest.raises(ExchangeRateError, match="Валюта GBP не поддерживается"):
        convert_amount_to_rubles(100.00, "GBP")


@patch("src.external_api.get_exchange_rate")
def test_convert_amount_to_rubles_rate_error(mock_get_rate) -> None:
    """Тестирование обработки ошибки получения курса"""
    # Настройка мока
    mock_get_rate.side_effect = ExchangeRateError("Ошибка получения курса")

    # Вызов функции и проверка исключения
    from src.external_api import convert_amount_to_rubles

    with pytest.raises(ExchangeRateError, match="Не удалось получить курс"):
        convert_amount_to_rubles(100.00, "USD")


@pytest.mark.skip(reason="Требуется реальный API ключ. Раскомментируйте для ручного тестирования.")
def test_integration_real_api():
    """
    Интеграционный тест с реальным API.
    Для запуска:
    1. Создайте .env файл с реальным ключом
    2. Раскомментируйте @pytest.mark.skip
    3. Запустите: pytest tests/test_external_api.py::test_integration_real_api -v
    """
    from src.external_api import convert_amount_to_rubles

    # Тест конвертации 100 USD в рубли
    result = convert_amount_to_rubles(100.00, "USD")

    # Проверяем, что результат разумный (курс обычно 70-100 руб за доллар)
    assert 7000 < result < 10000
    assert isinstance(result, float)
