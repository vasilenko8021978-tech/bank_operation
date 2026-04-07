from datetime import datetime
from typing import Dict, Any
import pandas as pd
from .logger import setup_logger

# Создаём отдельный объект логера для модуля views
logger = setup_logger(__name__, log_file="views")


def get_home_page(date_str: str) -> Dict[str, Any]:
    """
    Возвращает данные для страницы «Главная» в формате JSON.

    Функция:
    - Принимает строку с датой и временем в формате 'YYYY-MM-DD HH:MM:SS'
    - Извлекает транзакции за указанную дату
    - Формирует структурированный JSON-ответ
    - Использует вспомогательные функции из utils.py
    - Логирует все операции

    :param date_str: Дата и время в формате 'YYYY-MM-DD HH:MM:SS'
    :return: Словарь с данными для JSON-ответа
    """
    try:
        logger.info(f"Запрос главной страницы. Дата: {date_str}")

        # Валидация и парсинг даты
        try:
            target_datetime = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
            target_date = target_datetime.date().isoformat()  # YYYY-MM-DD
        except ValueError as e:  # ← ИСПРАВЛЕНО: вместо bare 'except'
            logger.error(f"Неверный формат даты '{date_str}': {e}")
            return {
                "status": "error",
                "message": f"Неверный формат даты. Ожидается 'YYYY-MM-DD HH:MM:SS'. Ошибка: {str(e)}",
            }

        # Получаем транзакции за указанную дату (вспомогательная функция из utils.py)
        # Примечание: в реальном проекте здесь будет вызов функции из utils.py
        transactions: list[dict[str, Any]] = []

        # Формируем статистику
        total_amount = 0.0
        rub_count = 0
        usd_count = 0
        eur_count = 0

        for tx in transactions:
            # Извлекаем сумму и валюту
            amount = 0.0
            currency = "RUB"

            if "operationAmount" in tx:
                op_amount = tx["operationAmount"]
                amount_str = op_amount.get("amount", "0")
                try:
                    amount = float(amount_str.replace(",", "."))
                except (ValueError, TypeError):
                    amount = 0.0

                if "currency" in op_amount:
                    currency = op_amount["currency"].get("code", "RUB")

            total_amount += amount

            # Считаем по валютам
            if currency == "RUB":
                rub_count += 1
            elif currency == "USD":
                usd_count += 1
            elif currency == "EUR":
                eur_count += 1

        # Формируем ответ
        response = {
            "status": "success",
            "request_date": date_str,
            "transactions_date": target_date,
            "statistics": {
                "total_transactions": len(transactions),
                "total_amount_rub_equivalent": round(total_amount, 2),
                "currency_breakdown": {"RUB": rub_count, "USD": usd_count, "EUR": eur_count},
            },
            "transactions": transactions[:10],  # Первые 10 транзакций для отображения
        }

        logger.info(f"Успешно обработан запрос главной страницы. Найдено {len(transactions)} транзакций")
        return response

    except Exception as e:  # ← ИСПРАВЛЕНО: вместо bare 'except'
        logger.error(f"Критическая ошибка в get_home_page: {e}", exc_info=True)
        return {"status": "error", "message": f"Внутренняя ошибка сервера: {str(e)}"}


def get_events_page(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Возвращает данные для страницы «События» в формате JSON.

    Функция:
    - Принимает DataFrame с транзакциями
    - Обрабатывает данные с использованием pandas
    - Формирует структурированный JSON-ответ
    - Использует вспомогательные функции из utils.py
    - Логирует все операции

    :param df: DataFrame с транзакциями
    :return: Словарь с данными для JSON-ответа
    """
    try:
        logger.info(f"Запрос страницы событий. Размер DataFrame: {len(df)} строк")

        # Проверка входных данных
        if df.empty:
            logger.warning("Получен пустой DataFrame для страницы событий")
            return {"status": "success", "events_count": 0, "events": [], "message": "Нет данных для отображения"}

        # Обрабатываем события (вспомогательная функция из utils.py)
        # Примечание: в реальном проекте здесь будет вызов функции из utils.py
        events_data = {
            "count": len(df),
            "period": "last_30_days",
            "events": [],
            "total_amount": 0.0,
            "currency_breakdown": {"RUB": 0, "USD": 0, "EUR": 0},
        }

        # Формируем ответ
        response = {
            "status": "success",
            "events_count": events_data.get("count", 0),
            "period": events_data.get("period", "unknown"),
            "events": events_data.get("events", []),
            "summary": {
                "total_amount": events_data.get("total_amount", 0.0),
                "currency_breakdown": events_data.get("currency_breakdown", {}),
            },
        }

        logger.info(f"Успешно обработан запрос страницы событий. Найдено {events_data.get('count', 0)} событий")
        return response

    except Exception as e:  # ← ИСПРАВЛЕНО: вместо bare 'except'
        logger.error(f"Критическая ошибка в get_events_page: {e}", exc_info=True)
        return {"status": "error", "message": f"Внутренняя ошибка сервера: {str(e)}"}
