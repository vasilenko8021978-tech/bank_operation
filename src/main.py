import sys
from typing import List, Dict, Any
from .utils import read_transactions_from_json
from .file_reader import read_csv_transactions, read_excel_transactions
from .processing import filter_by_state, sort_by_date
from .widget import mask_account_card
from .search import search_transactions_by_description
from .logger import setup_logger

# Создаём отдельный объект логера для модуля main
logger = setup_logger(__name__, log_file="main")


def get_user_choice(prompt: str, options: List[str]) -> str:
    """
    Получает выбор пользователя с валидацией.

    :param prompt: Текст запроса
    :param options: Список допустимых вариантов (в нижнем регистре)
    :return: Выбранный вариант в нижнем регистре
    """
    while True:
        user_input = input(prompt).strip().lower()
        if user_input in options:
            return user_input
        else:
            print(f"Неверный ввод. Допустимые варианты: {', '.join(options)}")


def get_transaction_amount(transaction: Dict[str, Any]) -> str:
    """
    Извлекает сумму и валюту из транзакции в форматированном виде.

    :param transaction: Словарь транзакции
    :return: Строка с суммой и валютой (например, "31957.58 руб.")
    """
    # Ищем сумму и валюту
    amount = ""
    currency = ""

    # Ищем ключ "operationAmount" с учётом пробелов
    operation_amount = {}
    for key, value in transaction.items():
        if isinstance(key, str) and key.strip() == "operationAmount":
            operation_amount = value if isinstance(value, dict) else {}
            break

    # Извлекаем сумму
    if operation_amount:
        for key, value in operation_amount.items():
            if isinstance(key, str) and key.strip() == "amount":
                amount = str(value).strip()
                break

    # Извлекаем валюту
    currency_info = {}
    for key, value in operation_amount.items():
        if isinstance(key, str) and key.strip() == "currency":
            currency_info = value if isinstance(value, dict) else {}
            break

    if currency_info:
        for key, value in currency_info.items():
            if isinstance(key, str) and key.strip() == "code":
                currency = str(value).strip()
                break

    # Форматируем вывод
    if currency.upper() == "RUB":
        return f"{amount} руб."
    else:
        return f"{amount} {currency}"


def format_transaction_date(date_str: str) -> str:
    """
    Форматирует дату из ISO формата в ДД.ММ.ГГГГ.

    :param date_str: Дата в формате ISO (2019-08-26T10:50:58.294041)
    :return: Дата в формате ДД.ММ.ГГГГ
    """
    try:
        # Извлекаем только дату (без времени)
        date_part = date_str.split("T")[0]
        year, month, day = date_part.split("-")
        return f"{day}.{month}.{year}"
    except :
        return date_str


def format_transaction(transaction: Dict[str, Any]) -> str:
    """
    Форматирует транзакцию для вывода в консоль.

    :param transaction: Словарь транзакции
    :return: Отформатированная строка с информацией о транзакции
    """
    # Извлекаем данные
    date = ""
    description = ""
    from_account = ""
    to_account = ""

    # Извлекаем дату
    for key, value in transaction.items():
        if isinstance(key, str) and key.strip() == "date":
            date = format_transaction_date(str(value).strip())
            break

    # Извлекаем описание
    for key, value in transaction.items():
        if isinstance(key, str) and key.strip() == "description":
            description = str(value).strip()
            break

    # Извлекаем отправителя (если есть)
    for key, value in transaction.items():
        if isinstance(key, str) and key.strip() == "from":
            from_account = mask_account_card(str(value).strip())
            break

    # Извлекаем получателя
    for key, value in transaction.items():
        if isinstance(key, str) and key.strip() == "to":
            to_account = mask_account_card(str(value).strip())
            break

    # Формируем вывод
    result = f"{date} {description}\n"

    if from_account:
        result += f"{from_account} -> {to_account}\n"
    else:
        result += f"{to_account}\n"

    result += f"Сумма: {get_transaction_amount(transaction)}\n"

    return result


def main() -> None:
    """
    Основная функция программы для работы с банковскими транзакциями.
    Реализует интерактивное меню для фильтрации и вывода транзакций.
    """
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    # Выбор формата файла
    file_choice = get_user_choice("Пользователь: ", ["1", "2", "3"])

    # Чтение данных
    transactions: List[Dict[str, Any]] = []
    if file_choice == "1":
        print("\nПрограмма: Для обработки выбран JSON-файл.")
        transactions = read_transactions_from_json("data/operations.json")
    elif file_choice == "2":
        print("\nПрограмма: Для обработки выбран CSV-файл.")
        transactions = read_csv_transactions("data/transactions.csv")
    else:  # file_choice == "3"
        print("\nПрограмма: Для обработки выбран XLSX-файл.")
        transactions = read_excel_transactions("data/transactions_excel.xlsx")

    if not transactions:
        print("Программа: Не удалось загрузить транзакции. Проверьте файл и повторите попытку.")
        return

    print(f"Программа: Загружено {len(transactions)} транзакций.")

    # Фильтрация по статусу
    valid_states = ["executed", "canceled", "pending"]
    while True:
        print("\nПрограмма: Введите статус, по которому необходимо выполнить фильтрацию.")
        print("Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING")

        state = input("Пользователь: ").strip().upper()

        if state.lower() in valid_states:
            filtered = filter_by_state(transactions, state)
            print(f'\nПрограмма: Операции отфильтрованы по статусу "{state}"')
            print(f"Найдено {len(filtered)} операций со статусом {state}.")
            transactions = filtered
            break
        else:
            print(f'Программа: Статус операции "{state}" недоступен.')

    # Сортировка по дате
    sort_choice = get_user_choice("\nПрограмма: Отсортировать операции по дате? Да/Нет\nПользователь: ", ["да", "нет"])

    if sort_choice == "да":
        order_choice = get_user_choice("Программа: Отсортировать по возрастанию или по убыванию?\nПользователь: ",
                                       ["по возрастанию", "по убыванию"])

        descending = order_choice == "по убыванию"
        transactions = sort_by_date(transactions, descending=descending)
        print(f"Программа: Операции отсортированы {('по убыванию' if descending else 'по возрастанию')}.")

    # Фильтрация по рублям
    ruble_choice = get_user_choice("\nПрограмма: Выводить только рублевые транзакции? Да/Нет\nПользователь: ",
                                   ["да", "нет"])

    if ruble_choice == "да":
        filtered = []
        for tx in transactions:
            # Ищем валюту
            currency = ""
            for key, value in tx.items():
                if isinstance(key, str) and key.strip() == "operationAmount":
                    if isinstance(value, dict):
                        for k, v in value.items():
                            if isinstance(k, str) and k.strip() == "currency":
                                if isinstance(v, dict):
                                    for ck, cv in v.items():
                                        if isinstance(ck, str) and ck.strip() == "code":
                                            currency = str(cv).strip().upper()
                                            break
                                    break
                        break
                    break

            if currency == "RUB":
                filtered.append(tx)

        print(f"Программа: Отфильтровано {len(filtered)} рублевых транзакций из {len(transactions)}.")
        transactions = filtered

    # Поиск по описанию
    search_choice = get_user_choice(
        "\nПрограмма: Отфильтровать список транзакций по определенному слову в описании? Да/Нет\nПользователь: ",
        ["да", "нет"])

    if search_choice == "да":
        search_query = input("Программа: Введите слово или регулярное выражение для поиска:\nПользователь: ").strip()

        if search_query:
            transactions = search_transactions_by_description(transactions, search_query)
            print(f"Программа: Найдено {len(transactions)} транзакций по запросу '{search_query}'.")

    # Вывод результатов
    print("\nПрограмма: Распечатываю итоговый список транзакций...\n")

    if not transactions:
        print("Программа: Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    print(f"Всего банковских операций в выборке: {len(transactions)}\n")

    for i, tx in enumerate(transactions[:5], 1):  # Выводим первые 5 транзакций
        print(format_transaction(tx))
        if i < len(transactions[:5]):
            print("-" * 50)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nПрограмма прервана пользователем.")
        sys.exit(0)
    except Exception as e:  # ← Исправлено: вместо bare 'except'
        logger.error(f"Критическая ошибка в основной программе: {e}", exc_info=True)
        print(f"\nПроизошла ошибка: {e}")
        sys.exit(1)

