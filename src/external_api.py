import os
from decimal import ROUND_HALF_UP, Decimal
from typing import Any, Dict, Optional, Union

# Объявляем флаг доступности библиотеки ОДИН РАЗ до try/except
REQUESTS_AVAILABLE: bool = False
RequestException: Any = Exception
Timeout: Any = Exception

# Импорт с обработкой ошибок
try:
    import requests
    from requests.exceptions import RequestException as ReqExc
    from requests.exceptions import Timeout as TimeoutExc

    REQUESTS_AVAILABLE = True
    RequestException = ReqExc
    Timeout = TimeoutExc
except ImportError:
    pass  # Библиотека недоступна, флаг остаётся False

# Загрузка переменных окружения
try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass  # python-dotenv не установлен


class ExchangeRateError(Exception):
    """Исключение для ошибок при получении курса валют"""

    pass


def get_exchange_rate(base_currency: str, target_currency: str) -> float:
    """
    Получает текущий курс обмена валют с использованием Exchange Rates Data API.

    :param base_currency: Базовая валюта (например, "USD")
    :param target_currency: Целевая валюта (например, "RUB")
    :return: Курс обмена (сколько целевой валюты за 1 единицу базовой)
    :raises ExchangeRateError: При ошибках запроса или обработки данных
    """
    if not REQUESTS_AVAILABLE:
        raise ExchangeRateError(
            "Библиотека 'requests' не установлена. Установите её: " "poetry add requests  или  pip install requests"
        )

    api_key: Optional[str] = os.getenv("EXCHANGE_RATES_API_KEY")
    if not api_key:
        raise ExchangeRateError("API ключ не найден. Установите EXCHANGE_RATES_API_KEY в файле .env")

    base_currency_clean: str = base_currency.upper().strip()
    target_currency_clean: str = target_currency.upper().strip()

    url: str = "https://api.apilayer.com/exchangerates_data/latest"
    params: Dict[str, str] = {"symbols": target_currency_clean, "base": base_currency_clean}
    headers: Dict[str, str] = {"apikey": api_key}

    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()

        data: Dict[str, Any] = response.json()

        # Проверяем успешность ответа API
        if not data.get("success", False):
            error_info: str = data.get("error", {}).get("info", "Неизвестная ошибка API")
            raise ExchangeRateError(f"Ошибка API: {error_info}")

        # Извлекаем курс из ответа
        rates: Dict[str, float] = data.get("rates", {})
        rate: Optional[float] = rates.get(target_currency_clean)

        if rate is None:
            raise ExchangeRateError(f"Курс для валюты {target_currency_clean} не найден в ответе API")

        return float(rate)

    except Timeout:
        raise ExchangeRateError("Таймаут запроса к API обменных курсов")
    except RequestException as e:
        raise ExchangeRateError(f"Ошибка сети при запросе к API: {str(e)}")
    except ValueError as e:
        raise ExchangeRateError(f"Ошибка парсинга ответа API: {str(e)}")


def convert_amount_to_rubles(amount: Union[float, str, Decimal], currency_code: str) -> float:
    """
    Конвертирует сумму из указанной валюты в рубли.

    :param amount: Сумма для конвертации (может быть строкой, числом или Decimal)
    :param currency_code: Код исходной валюты ("RUB", "USD", "EUR")
    :return: Сумма в рублях (округленная до 2 знаков)
    :raises ExchangeRateError: При ошибках получения курса или конвертации
    """
    # Преобразуем сумму в Decimal для точных вычислений
    if isinstance(amount, str):
        amount_clean: str = amount.replace(",", ".")
        amount_decimal: Decimal = Decimal(amount_clean)
    elif isinstance(amount, float):
        amount_decimal = Decimal(str(amount))
    elif isinstance(amount, Decimal):
        amount_decimal = amount
    else:
        raise ValueError(f"Неподдерживаемый тип суммы: {type(amount)}")

    currency_code_clean: str = currency_code.upper().strip()

    # Если валюта уже в рублях — возвращаем сумму как есть
    if currency_code_clean == "RUB":
        return float(amount_decimal.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))

    # Поддерживаемые валюты для конвертации
    supported_currencies: set[str] = {"USD", "EUR"}
    if currency_code_clean not in supported_currencies:
        raise ExchangeRateError(
            f"Валюта {currency_code_clean} не поддерживается для конвертации. "
            f"Поддерживаются: {', '.join(sorted(supported_currencies))}"
        )

    # Получаем курс обмена
    try:
        rate: float = get_exchange_rate(currency_code_clean, "RUB")
        rate_decimal: Decimal = Decimal(str(rate))
    except ExchangeRateError as e:
        raise ExchangeRateError(f"Не удалось получить курс {currency_code_clean} к RUB: {str(e)}")

    # Конвертируем сумму
    rub_amount: Decimal = amount_decimal * rate_decimal

    # Округляем до 2 знаков после запятой
    return float(rub_amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def get_transaction_amount_in_rubles(transaction: Dict[str, Any]) -> float:
    """
    Извлекает сумму транзакции и конвертирует её в рубли.

    :param transaction: Словарь с данными транзакции
    :return: Сумма транзакции в рублях
    :raises ValueError: Если транзакция имеет неверную структуру
    :raises ExchangeRateError: При ошибках конвертации
    """

    # Рекурсивная функция для очистки всех ключей и значений
    def clean_data_recursive(data: Any) -> Any:
        if isinstance(data, dict):
            cleaned_dict = {}
            for key, value in data.items():
                cleaned_key = key.strip() if isinstance(key, str) else key
                cleaned_dict[cleaned_key] = clean_data_recursive(value)
            return cleaned_dict
        elif isinstance(data, list):
            return [clean_data_recursive(item) for item in data]
        elif isinstance(data, str):
            return data.strip()
        else:
            return data

    # Очищаем ВСЕ ключи и значения в транзакции
    cleaned_transaction = clean_data_recursive(transaction)

    # Пропускаем пустые транзакции
    if not cleaned_transaction:
        raise ValueError("Пустая транзакция")

    # Извлекаем сумму
    try:
        operation_amount = cleaned_transaction.get("operationAmount", {})
        if not isinstance(operation_amount, dict):
            raise ValueError("Поле 'operationAmount' должно быть словарём")

        amount_str = str(operation_amount.get("amount", "")).strip()
        if not amount_str:
            raise ValueError("Сумма транзакции не указана")

        # Извлекаем код валюты
        currency = operation_amount.get("currency", {})
        if not isinstance(currency, dict):
            raise ValueError("Поле 'currency' должно быть словарём")

        currency_code = str(currency.get("code", "")).strip()
        if not currency_code:
            raise ValueError("Код валюты не указан")

        # Конвертируем в рубли
        return convert_amount_to_rubles(amount_str, currency_code)

    except (ValueError, TypeError) as e:
        raise ValueError(f"Ошибка при обработке транзакции: {str(e)}")
