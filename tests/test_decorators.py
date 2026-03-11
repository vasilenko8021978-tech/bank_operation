import pytest
import os
from src.decorators import log
from src.widget import mask_account_card


def test_log_decorator_with_timestap_console(capsys):
    """Тестирование логирования с временной меткой в консоль"""

    @log()
    def add(x: int, y: int) -> int:
        return x + y

    # Вызываем функцию
    result = add(1, 2)

    # Проверяем результат
    assert result == 3

    # Перехватываем вывод в консоль
    captured = capsys.readouterr()

    # Проверяем, что в выводе есть временная метка
    assert "[" in captured.out
    assert "]" in captured.out
    assert "add ok" in captured.out

    # Проверяем формат временной метки (ГГГГ-ММ-ДД ЧЧ:ММ:СС)
    import re

    timestamp_pattern = r"\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\]"
    assert re.search(timestamp_pattern, captured.out)


def test_log_decorator_with_timestamp_file():
    """Тестирование логирования с временной меткой в файл"""
    log_file = "test_timestamp.log"

    @log(filename=log_file)
    def add(x, y):
        return x + y

        # Вызываем функцию
        result = add(1, 2)

        # Проверяем результат
        assert result == 3

        # Проверяем содержимое файла
        with open(log_file, "r", encoding="utf-8") as f:
            content = f.read()
            assert "[" in content
            assert "]" in content
            assert "add ok" in content

        # Удаляем тестовый файл
        os.remove(log_file)


# ===== ТЕСТЫ ДЛЯ mask_account_card С ДЕКОРАТОРОМ =====


def test_mask_account_card_with_log_decorator_success(capsys):
    """Тестирование функции mask_account_card с декоратором @log при успешном выполнении"""

    # Создаём декорированную версию функции
    @log()
    def decorated_mask_account_card(number: str) -> str:
        return mask_account_card(number)

    # Вызываем функцию
    result = decorated_mask_account_card("Visa 1234567890123456")

    # Проверяем результат
    assert result == "Visa 1234 56** **** 3456"

    # Перехватываем вывод в консоль
    captured = capsys.readouterr()

    # Проверяем, что в выводе есть сообщение об успешном выполнении
    assert "decorated_mask_account_card ok" in captured.out


def test_mask_account_card_with_log_decorator_card_number(capsys):
    """Тестирование маскирования номера карты с декоратором"""

    @log()
    def decorated_mask_account_card(number: str) -> str:
        return mask_account_card(number)

    # Тестируем разные форматы карт
    result1 = decorated_mask_account_card("MasterCard 9876543210987654")
    assert result1 == "MasterCard 9876 54** **** 7654"

    result2 = decorated_mask_account_card("Maestro 1234567890123456")
    assert result2 == "Maestro 1234 56** **** 3456"

    # Перехватываем вывод в консоль
    captured = capsys.readouterr()

    # Проверяем, что все вызовы залогированы
    assert captured.out.count("decorated_mask_account_card ok") == 2


def test_mask_account_card_with_log_decorator_account(capsys):
    """Тестирование маскирования номера счёта с декоратором"""

    @log()
    def decorated_mask_account_card(number: str) -> str:
        return mask_account_card(number)

    # Вызываем функцию для счёта
    result = decorated_mask_account_card("Счет 73654108430135874305")

    # Проверяем результат
    assert result == "Счет **4305"

    # Перехватываем вывод в консоль
    captured = capsys.readouterr()

    # Проверяем, что в выводе есть сообщение об успешном выполнении
    assert "decorated_mask_account_card ok" in captured.out


def test_mask_account_card_with_log_decorator_empty_string(capsys):
    """Тестирование обработки пустой строки с декоратором"""

    @log()
    def decorated_mask_account_card(number: str) -> str:
        return mask_account_card(number)

    # Вызываем функцию с пустой строкой
    result = decorated_mask_account_card("")

    # Проверяем результат
    assert result == "Ошибка: пустая строка"

    # Перехватываем вывод в консоль
    captured = capsys.readouterr()

    # Проверяем, что в выводе есть сообщение об успешном выполнении
    # (функция вернула результат, а не выбросила исключение)
    assert "decorated_mask_account_card ok" in captured.out


def test_mask_account_card_with_log_decorator_invalid_format(capsys):
    """Тестирование обработки неверного формата с декоратором"""

    @log()
    def decorated_mask_account_card(number: str) -> str:
        return mask_account_card(number)

    # Вызываем функцию с неверным форматом
    result = decorated_mask_account_card("Неправильный")

    # Проверяем результат
    assert result == "Ошибка: отсутствует название карты или счета"

    # Перехватываем вывод в консоль
    captured = capsys.readouterr()

    # Проверяем, что в выводе есть сообщение об успешном выполнении
    assert "decorated_mask_account_card ok" in captured.out


def test_mask_account_card_with_log_decorator_non_digit(capsys):
    """Тестирование обработки нецифровых символов с декоратором"""

    @log()
    def decorated_mask_account_card(number: str) -> str:
        return mask_account_card(number)

    # Вызываем функцию с нецифровыми символами
    result = decorated_mask_account_card("Visa abc123")

    # Проверяем результат
    assert result == "Ошибка: номер содержит нецифровые символы"

    # Перехватываем вывод в консоль
    captured = capsys.readouterr()

    # Проверяем, что в выводе есть сообщение об успешном выполнении
    assert "decorated_mask_account_card ok" in captured.out


# ===== ТЕСТЫ ДЛЯ ЛОГИРОВАНИЯ В ФАЙЛ =====


def test_mask_account_card_with_log_to_file():
    """Тестирование логирования mask_account_card в файл"""
    log_file = "test_mask_card.log"

    @log(filename=log_file)
    def decorated_mask_account_card(number: str) -> str:
        return mask_account_card(number)

    # Вызываем функцию
    result = decorated_mask_account_card("Visa 1234567890123456")

    # Проверяем результат
    assert result == "Visa 1234 56** **** 3456"

    # Проверяем содержимое файла
    with open(log_file, "r", encoding="utf-8") as f:
        content = f.read()
        assert "decorated_mask_account_card ok" in content

    # Удаляем тестовый файл
    import os

    os.remove(log_file)


# ===== ТЕСТЫ ДЛЯ ОШИБОК =====


def test_mask_account_card_with_log_decorator_and_error(capsys):
    """Тестирование обработки ошибок в mask_account_card с декоратором"""

    @log()
    def decorated_mask_account_card(number: str) -> str:
        # Искусственно вызываем ошибку
        if not isinstance(number, str):
            raise TypeError("Номер должен быть строкой")
        return mask_account_card(number)

    # Вызываем функцию с ошибкой
    with pytest.raises(TypeError):
        decorated_mask_account_card(12345)  # Передаём число вместо строки

    # Перехватываем вывод в консоль
    captured = capsys.readouterr()

    # Проверяем, что в выводе есть сообщение об ошибке
    assert "decorated_mask_account_card error: TypeError" in captured.out
    assert "Inputs: (12345,)" in captured.out
