from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(number: str) -> str:
    """Функция, которая умеет обрабатывать информацию как о картах, так и о счетах."""
    number = number.strip()
    """ Проверка пустой строки"""
    if not number:
        return "Ошибка: пустая строка"
    parts = number.split()

    # Проверка наличия номера
    if len(parts) < 2:
        return "Ошибка: отсутствует название карты или счета"

    # Проверка, что номер состоит только из цифр
    if not parts[-1].isdigit():
        return "Ошибка: номер содержит нецифровые символы"

    if "счет" in number.lower():
        return f"Счет {get_mask_account(number.split()[-1])}"
    else:
        card_name = " ".join(number.split()[:-1])
        card_mask = get_mask_card_number(number.split()[-1])

        clean_name = card_name.replace(" ", "")
        if not clean_name.isalpha() or len(clean_name) < 4:
            return "Неправильно введено название счета(карты)"

    return f"{card_name} {card_mask}"


def get_date(date: str) -> str:
    """Преобразует дату из формата '2024-03-11T02:26:18.671407' в '11.03.2024'"""
    date = date.strip()

    # Проверка пустой строки
    if not date:
        return "Некорректный формат даты"

    # Минимальная длина и проверка разделителей "-"
    if len(date) < 10 or date[4] != "-" or date[7] != "-":
        return "Некорректный формат даты"

    # Минимальная длина и проверка разделителей '-'
    if len(date) < 10 or date[4] != "-" or date[7] != "-":
        return "Некорректный формат даты"

    try:
        year = date[:4]
        month = date[5:7]
        day = date[8:10]

        # Проверка, что части даты - цифры
        if not (year.isdigit() and month.isdigit() and day.isdigit()):
            return "Некорректный формат даты"
        # Базовая валидация диапазонов
        if not (1 <= int(month) <= 12 and 1 <= int(day) <= 31):
            return "Некорректный формат даты"

        return f"{day}.{month}.{year}"

    except (IndexError, ValueError):
        return "Некорректный формат даты"
