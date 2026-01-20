def filter_by_state(list_dict: list[dict], state: str = 'EXECUTED') -> list:
    """Функция, которая принимает список словарей и опционально значение для ключа"""
    filtered_list = []
    for item in list_dict:
        if item["state"] == state:
            filtered_list.append(item)
    return filtered_list


def sort_by_date(list_dict: list[dict]) -> list :
    """ Функция, которая принимает список словарей и необязательный параметр, задающий порядок сортировки
    (по умолчанию — убывание) и возвращает новый список, отсортированный по дате """
    sorted_list = sorted(list_dict, key=lambda x: x['date'], reverse = True)
    return sorted_list


if __name__ == '__main__':
    i = [{'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
         {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
         {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
         {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}]
    print(sort_by_date(i))
