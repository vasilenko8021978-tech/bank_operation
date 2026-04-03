from pathlib import Path
from typing import Any, Dict, List

import pandas as pd

from .logger import setup_logger

# Создаём отдельный объект логера для модуля file_reader
logger = setup_logger(__name__, log_file="file_reader")


def read_csv_transactions(file_path: str) -> List[Dict[str, Any]]:
    """
    Считывает финансовые операции из CSV-файла и возвращает список словарей.

    Функция обрабатывает:
    - Очистку ключей и значений от пробелов
    - Преобразование плоской структуры во вложенную (operationAmount, currency)
    - Пропуск пустых строк
    - Обработку ошибок чтения

    :param file_path: Путь к CSV-файлу
    :return: Список словарей с транзакциями в формате, совместимом с JSON-структурой.
             Возвращает пустой список при ошибке или отсутствии файла.
    """
    try:
        logger.debug(f"Начато чтение CSV файла: {file_path}")

        # Проверяем существование файла
        if not Path(file_path).exists():
            logger.error(f"CSV файл не найден: {file_path}")
            return []

        # Читаем CSV файл с помощью pandas
        df = pd.read_csv(file_path, encoding='utf-8-sig')  # utf-8-sig для обработки BOM
        logger.info(f"Успешно прочитано {len(df)} строк из CSV файла {file_path}")

        # Заменяем NaN на пустые строки
        df = df.fillna('')

        transactions: List[Dict[str, Any]] = []
        for _, row in df.iterrows():
            # Преобразуем строку в словарь (row уже является объектом, похожим на словарь)
            # Для совместимости с моками используем to_dict() если доступен, иначе преобразуем вручную
            try:
                transaction = row.to_dict()
            except AttributeError:
                # Если row не имеет to_dict() (как в моках), используем напрямую
                transaction = dict(row)

            # Очищаем ключи и значения от пробелов
            cleaned_transaction = _clean_data_recursive(transaction)

            # Пропускаем пустые транзакции
            if not cleaned_transaction or all(not v for v in cleaned_transaction.values()):
                continue

            # Формируем вложенную структуру operationAmount
            cleaned_transaction = _build_nested_structure(cleaned_transaction)

            transactions.append(cleaned_transaction)

        logger.info(f"Обработано {len(transactions)} транзакций из CSV файла")
        return transactions

    except pd.errors.EmptyDataError:
        logger.error(f"CSV файл пустой: {file_path}")
        return []
    except pd.errors.ParserError as e:
        logger.error(f"Ошибка парсинга CSV файла {file_path}: {e}")
        return []
    except Exception as e:
        logger.error(f"Ошибка при чтении CSV файла {file_path}: {e}", exc_info=True)
        return []


def read_excel_transactions(file_path: str) -> List[Dict[str, Any]]:
    """
    Считывает финансовые операции из Excel-файла (XLSX) и возвращает список словарей.

    Функция обрабатывает:
    - Очистку ключей и значений от пробелов
    - Преобразование плоской структуры во вложенную (operationAmount, currency)
    - Пропуск пустых строк
    - Обработку ошибок чтения

    :param file_path: Путь к Excel-файлу (формат .xlsx)
    :return: Список словарей с транзакциями в формате, совместимом с JSON-структурой.
             Возвращает пустой список при ошибке или отсутствии файла.
    """
    try:
        logger.debug(f"Начато чтение Excel файла: {file_path}")

        # Проверяем существование файла
        if not Path(file_path).exists():
            logger.error(f"Excel файл не найден: {file_path}")
            return []

        # Читаем Excel файл с помощью pandas
        df = pd.read_excel(file_path, engine='openpyxl')
        logger.info(f"Успешно прочитано {len(df)} строк из Excel файла {file_path}")

        # Заменяем NaN на пустые строки
        df = df.fillna('')

        transactions: List[Dict[str, Any]] = []
        for _, row in df.iterrows():
            # Преобразуем строку в словарь
            try:
                transaction = row.to_dict()
            except AttributeError:
                transaction = dict(row)

            # Очищаем ключи и значения от пробелов
            cleaned_transaction = _clean_data_recursive(transaction)

            # Пропускаем пустые транзакции
            if not cleaned_transaction or all(not v for v in cleaned_transaction.values()):
                continue

            # Формируем вложенную структуру operationAmount
            cleaned_transaction = _build_nested_structure(cleaned_transaction)

            transactions.append(cleaned_transaction)

        logger.info(f"Обработано {len(transactions)} транзакций из Excel файла")
        return transactions

    except ValueError as e:
        logger.error(f"Ошибка чтения Excel файла {file_path}: {e}")
        return []
    except Exception as e:
        logger.error(f"Ошибка при чтении Excel файла {file_path}: {e}", exc_info=True)
        return []


def _clean_data_recursive(data: Any) -> Any:
    """
    Рекурсивно очищает ключи и строковые значения от пробелов.

    :param  Данные для очистки
    :return: Очищенные данные
    """
    if isinstance(data, dict):
        cleaned_dict: Dict[str, Any] = {}
        for key, value in data.items():
            cleaned_key = key.strip() if isinstance(key, str) else key
            cleaned_dict[cleaned_key] = _clean_data_recursive(value)
        return cleaned_dict
    elif isinstance(data, list):
        return [_clean_data_recursive(item) for item in data]
    elif isinstance(data, str):
        return data.strip()
    else:
        return data


def _build_nested_structure(transaction: Dict[str, Any]) -> Dict[str, Any]:
    """
    Формирует вложенную структуру из плоских полей:
    - Объединяет amount, currency_name, currency_code в operationAmount.currency
    - Сохраняет совместимость с форматом operations.json

    :param transaction: Словарь транзакции с плоской структурой
    :return: Обновленный словарь с вложенной структурой
    """
    # Создаем копию, чтобы не изменять оригинал
    result = transaction.copy()

    # Проверяем наличие полей для формирования вложенной структуры
    has_amount = 'amount' in result
    has_currency_name = 'currency_name' in result
    has_currency_code = 'currency_code' in result

    if has_amount or has_currency_name or has_currency_code:
        # Создаем вложенную структуру
        operation_amount: Dict[str, Any] = {}

        # Добавляем сумму, если есть
        if has_amount:
            operation_amount['amount'] = result.pop('amount')

        # Добавляем валюту, если есть хотя бы одно поле валюты
        if has_currency_name or has_currency_code:
            currency: Dict[str, str] = {}
            if has_currency_name:
                currency['name'] = result.pop('currency_name')
            if has_currency_code:
                currency['code'] = result.pop('currency_code')
            operation_amount['currency'] = currency

        # Добавляем вложенную структуру в транзакцию
        result['operationAmount'] = operation_amount

    return result
