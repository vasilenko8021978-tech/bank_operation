from src.widget import mask_account_card, get_date
import pytest


@pytest.mark.parametrize("input_data, expected_output", [
    ("Счет 73654108430135874305", "Счет **4305"),
    ("счет 1234", "Счет количество цифр не равно 20"),
    ("Visa 1234567890123456", "Visa 1234 56** **** 3456"),
    ("MasterCard 9876543210987654", "MasterCard 9876 54** **** 7654"),
    ("", "Ошибка: пустая строка"),
    ("   ", "Ошибка: пустая строка"),
    ("Счет", "Ошибка: отсутствует название карты или счета"),
    ("1234567890123456", "Ошибка: отсутствует название карты или счета"),
    ("Счет abc", "Ошибка: номер содержит нецифровые символы"),
    ("Vis 1234567812345678", "Неправильно введено название счета(карты)"),
])
def test_mask_account_card(input_data: str, expected_output: str)->None:
    assert mask_account_card(input_data) == expected_output


@pytest.mark.parametrize("input_date, expected_output", [
    # Позитивные сценарии
    ("2024-03-11T02:26:18.671407", "11.03.2024"),
    ("2023-12-31T23:59:59.999999", "31.12.2023"),
    ("2000-01-01T00:00:00.000000", "01.01.2000"),
    ("1999-09-09T12:34:56.789012", "09.09.1999"),

    # Негативные сценарии
    ("2024/01/01T00:00:00", "Некорректный формат даты"),  # неверный разделитель
    ("корректная строка", "Некорректный формат даты"),  # не дата вообще
    ("2024-01", "Некорректный формат даты"),  # неполная дата
])
def test_get_date(input_date: str, expected_output: str)->None:
    assert get_date(input_date) == expected_output


def test_get_date_short_string()->None:
    """Короткая строка (< 10 символов)"""
    # Строка длиной 9 символов - должно сработать условие len(date) < 10
    assert get_date("2024-01-0") == "Некорректный формат даты"


def test_get_date_wrong_separator_at_position_4()->None:
    """Неверный разделитель на позиции 4"""
    # На позиции 4 должен быть '-', но здесь '/'
    assert get_date("2024/01-01T00:00:00") == "Некорректный формат даты"


def test_get_date_wrong_separator_at_position_7()->None:
    """ Неверный разделитель на позиции 7"""
    assert get_date("2024-01.01T00:00:00") == "Некорректный формат даты"


def test_get_date_index_error_in_try_block()->None:
    """ Вызовет IndexError внутри блока try"""
    # Создаём ситуацию, которая вызовет IndexError при срезе
    assert get_date("2024-01-01") == "01.01.2024"