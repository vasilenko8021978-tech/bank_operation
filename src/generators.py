from typing import Generator


def transaction_generator(transactions: list) -> Generator:
    """
    Генератор для построчной обработки транзакций.

    :param transactions: Список транзакций
    :yield: Каждая транзакция по очереди
    """
    for transaction in transactions:
        yield transaction


def batch_generator(transactions: list, batch_size: int = 10) -> Generator:
    """
    Генератор для обработки транзакций пакетами.

    :param transactions: Список транзакций
    :param batch_size: Размер пакета
    :yield: Пакет транзакций
    """
    for i in range(0, len(transactions), batch_size):
        yield transactions[i : i + batch_size]


def filter_generator(transactions: list, min_amount: float = 0, max_amount: float = float("inf")) -> Generator:
    """
    Генератор для фильтрации транзакций по сумме.

    :param transactions: Список транзакций
    :param min_amount: Минимальная сумма
    :param max_amount: Максимальная сумма
    :yield: Отфильтрованные транзакции
    """
    for transaction in transactions:
        # Извлекаем сумму из транзакции
        amount = 0.0
        if "operationAmount" in transaction:
            op_amount = transaction["operationAmount"]
            amount_str = op_amount.get("amount", "0")
            try:
                amount = float(amount_str.replace(",", "."))
            except (ValueError, TypeError):
                amount = 0.0

        # Проверяем условия фильтрации
        if min_amount <= amount <= max_amount:
            yield transaction
