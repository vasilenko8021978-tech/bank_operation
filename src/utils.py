import json
import os
from typing import List, Dict, Any


def clean_transaction_data(data: Any) -> Any:
    """
    Рекурсивно очищает ВСЕ ключи и строковые значения от пробелов.

    :param data: Данные для очистки
    :return: Очищенные данные
    """
    if isinstance(data, dict):
        cleaned_dict = {}
        for key, value in data.items():
            cleaned_key = key.strip() if isinstance(key, str) else key
            cleaned_value = clean_transaction_data(value)
            cleaned_dict[cleaned_key] = cleaned_value
        return cleaned_dict
    elif isinstance(data, list):
        return [clean_transaction_data(item) for item in data]
    elif isinstance(data, str):
        return data.strip()
    else:
        return data


def read_transactions_from_json(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает данные о финансовых транзакциях из JSON-файла.
    ГАРАНТИРОВАННО очищает ВСЕ ключи и значения от пробелов.

    :param file_path: Путь до JSON-файла
    :return: Список словарей с данными о транзакциях.
             Возвращает пустой список, если файл пустой, не содержит список или не найден.
    """
    try:
        # Проверяем существование файла
        if not os.path.exists(file_path):
            print(f"Файл не найден: {file_path}")
            return []

        # Открываем и читаем файл
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read().strip()

            # Проверяем, что файл не пустой
            if not content:
                print(f"Файл пустой: {file_path}")
                return []

            # Парсим JSON
            data = json.loads(content)

            # Проверяем, что данные являются списком
            if isinstance(data, list):
                # Полная очистка всех данных
                cleaned_data = []
                for transaction in data:
                    # Пропускаем пустые объекты (как {} в конце файла)
                    if not transaction or not isinstance(transaction, dict):
                        continue

                    # Очищаем транзакцию
                    cleaned_transaction = clean_transaction_data(transaction)
                    cleaned_data.append(cleaned_transaction)

                return cleaned_data
            else:
                print(f"Файл не содержит список: {file_path}")
                return []

    except json.JSONDecodeError as e:
        print(f"Ошибка парсинга JSON: {e}")
        return []

    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return []
