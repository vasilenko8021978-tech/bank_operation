def filter_by_state(list_dict: list[dict], state: str = "EXECUTED") -> list:
    """Функция, которая принимает список словарей и опционально значение для ключа"""
    filtered_list = []
    for item in list_dict:
        if item["state"] == state:
            filtered_list.append(item)
    return filtered_list


def sort_by_date(list_dict: list[dict], reduce: bool=True) -> list:
    """Функция, которая принимает список словарей и необязательный параметр, задающий порядок сортировки
    (по умолчанию — убывание) и возвращает новый список, отсортированный по дате"""
    sorted_list = sorted(list_dict, key=lambda x: x["date"], reverse=reduce)
    return sorted_list