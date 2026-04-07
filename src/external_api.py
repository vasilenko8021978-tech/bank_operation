import os

import requests
from requests.exceptions import RequestException, Timeout
from dotenv import load_dotenv

from .logger import setup_logger

# Создаём логер
logger = setup_logger(__name__, log_file="external_api")


class ExchangeRateError(Exception):
    """Исключение для ошибок получения курса валют."""

    pass


def get_exchange_rate(base_currency: str, target_currency: str) -> float:
    """
    Получает курс обмена валют с использованием API.

    :param base_currency: Базовая валюта (например, "USD")
    :param target_currency: Целевая валюта (например, "RUB")
    :return: Курс обмена
    :raises ExchangeRateError: При ошибках получения курса
    """
    try:
        # Загружаем переменные окружения
        load_dotenv()

        # Получаем API ключ из переменных окружения
        api_key = os.getenv("EXCHANGE_RATES_API_KEY")
        if not api_key:
            logger.error("API ключ для обменных курсов не найден в .env")
            raise ExchangeRateError("API ключ не настроен")

        # Формируем URL запроса
        url = f"https://api.exchangerate-api.com/v4/latest/{base_currency}"

        # Выполняем запрос
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        # Парсим ответ
        data = response.json()
        rates = data.get("rates", {})

        if target_currency not in rates:
            logger.error(f"Валюта {target_currency} не найдена в ответе API")
            raise ExchangeRateError(f"Валюта {target_currency} не поддерживается")

        rate = rates[target_currency]
        logger.info(f"Получен курс: 1 {base_currency} = {rate} {target_currency}")
        return float(rate)

    except (RequestException, Timeout) as e:
        logger.error(f"Ошибка при запросе к API обменных курсов: {e}")
        raise ExchangeRateError(f"Ошибка подключения к API: {str(e)}")
    except ValueError as e:
        logger.error(f"Ошибка парсинга ответа API: {e}")
        raise ExchangeRateError(f"Некорректный ответ от API: {str(e)}")
    except Exception as e:
        logger.error(f"Неожиданная ошибка при получении курса: {e}", exc_info=True)
        raise ExchangeRateError(f"Внутренняя ошибка: {str(e)}")
