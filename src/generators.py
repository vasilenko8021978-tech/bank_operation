from typing import Any, Dict, Iterator, List


def filter_by_currency(transactions: List[Dict[str, Any]], currency_code: str) -> Iterator[Dict[str, Any]]:
    """Функция, принимает на вход список словарей, представляющих транзакции
    и возвращает итератор, который поочередно выдает транзакции, где валюта
    операции соответствует заданной"""
    for transaction in transactions:
        try:
            if (
                "operationAmount" in transaction
                    and "currency" in transaction["operationAmount"] and
                    "code" in transaction["operationAmount"]["currency"]
            ):
                # Сравниваем код валюты (регистронезависимо и без пробелов)
                tx_currency = transaction["operationAmount"]["currency"]["code"].strip()
                if not tx_currency:
                    continue

                if tx_currency.upper() == currency_code.upper():
                    yield transaction
        except (KeyError, TypeError):
            continue


def transaction_description(transactions: List[Dict[str, Any]]) -> Iterator[Dict[str, Any]]:
    """Генератор, который возвращает описание каждой транзакции по очереди"""
    for transaction in transactions:
        try:
            # Извлекаем описание транзакции
            description = transaction.get("description", "Без описания")
            yield description
        except (KeyError, TypeError, AttributeError):
            # Пропускаем транзакции с некорректной структурой
            continue


def card_number_generator(start: int, end: int) -> Iterator[str]:
    """
    Генератор, который выдает номера банковских карт в формате 'XXXX XXXX XXXX XXXX'
    :param start: Начальное значение диапазона (включительно)
    :param end: Конечное значение диапазона (включительно)
    :return: Итератор строк с номерами карт
    :raises ValueError: Если start < 1, end > 9999999999999999 или start > end
    """
    # Проверка валидности входных данных
    MIN_CARD_NUMBER = 1
    MAX_CARD_NUMBER = 9999999999999999

    if start < MIN_CARD_NUMBER:
        raise ValueError(f"Начальное значение должно быть >= {MIN_CARD_NUMBER}")
    if end > MAX_CARD_NUMBER:
        raise ValueError(f"Конечное значение должно быть <= {MAX_CARD_NUMBER}")
    if start > end:
        raise ValueError("Начальное значение не может быть больше конечного")

    # Генерация номеров карт
    for number in range(start, end + 1):
        # Форматируем номер: заполняем нулями до 16 цифр
        card_str = str(number).zfill(16)

        # Форматируем в виде 'ХХХХ ХХХХ ХХХХ ХХХХ'
        formatted = f"{card_str[:4]} {card_str[4:8]} {card_str[8:12]} {card_str[12:]}"
        yield formatted
