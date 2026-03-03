import pytest
from src.generators import filter_by_currency, transaction_description, card_number_generator


"""Фикстура с тестовыми транзакциями"""
@pytest.fixture
def sample_transaction():
    return [
        {
            "id": 1,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {
                "amount": "9824.07",
                "currency": {"name": "USD", "code": "USD"}
            },
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702"},
    {
            "id": 2,
            "state": "EXECUTED",
        "date": "2019-04-04T23:20:05.206878",
        "operationAmount":
            {"amount": "79114.93",
             "currency": {"name": "USD", "code": "USD"}
            },
        "description": "Перевод со счета на счет",
        "from": "Счет 19708645243227258542",
        "to": "Счет 75651667383060284188"
    },
    {
        "id": 3,
        "state": "EXECUTED",
        "date": "2019-03-23T01:09:46.296404",
        "operationAmount": {
            "amount": "43318.34",
            "currency": {"name": "RUB", "code": "RUB"}
    },
        "description": "Перевод со счета на счет",
        "from": "Счет 44812258784861134719",
        "to": "Счет 74489636417521191164"
    },
    {
        "id": 4,
        "state": "EXECUTED",
        "date": "2019-07-03T18:35:29.512364",
        "operationAmount": {
            "amount": "8221.37",
            "currency": {"name": "USD", "code": "USD"}
        },
        "description": "Перевод организации",
        "from": "MasterCard 1234567890123456",
        "to": "Счет 12345678901234567890"
        },
    {
        "id": 5,
        "state": "CANCELED",
        "date": "2019-08-26T10:50:58.294041",
        "operationAmount": {
            "amount": "65432.10",
            "currency": {"name": "EUR", "code": "EUR"}
        },
        "description": "Перевод с карты на карту",
        "from": "Visa 1234567812345678",
        "to": "MasterCard 1234567890123456"
    }
    ]


def test_filter_by_currency_usd(sample_transaction):
    """Тестирование фильтрации транзакций в USD"""
    usd_transactions = list( filter_by_currency(sample_transaction,"USD"))

    #Проверяем количество транзакций
    assert len(usd_transactions) == 3

    #Проверяем, что все транзакции имеют код валюты USD
    assert all(
        tx["operationAmount"]["currency"]["code"] == "USD"
        for tx in usd_transactions
    )
    #Проверяем конкретные ID
    usd_ids = {tx["id"] for tx in usd_transactions}
    assert usd_ids == {1, 2, 4}


def test_filter_by_currency_eur(sample_transaction):
    """Тестирование фильтрации транзакций в EUR """
    eur_transactions = list( filter_by_currency(sample_transaction,"EUR"))
    assert len(eur_transactions) == 1
    assert eur_transactions[0]["id"] == 5
    assert eur_transactions[0]["operationAmount"]["currency"]["code"] == "EUR"


def test_filter_by_currency_rub(sample_transaction):
    """ Тестирование фильтрации транзакции в RUB"""
    rub_transactions = list( filter_by_currency(sample_transaction,"RUB"))
    assert len(rub_transactions) == 1
    assert rub_transactions[0]["id"] == 3
    assert rub_transactions[0]["operationAmount"]["currency"]["code"] == "RUB"


def test_filter_by_currency_no_matches(sample_transaction):
    """ Тестирование фильтрации, когда транзакции в заданной валюте отсутствуют"""
    gbr_transactions = list( filter_by_currency(sample_transaction,"GBR"))
    assert len(gbr_transactions) == []


def test_filter_by_currency_empty_list(sample_transaction):
    """ Тестирование работы с пустым списком"""
    empty_list = []
    result = list( filter_by_currency(empty_list, "USD"))
    assert result == []


def test_filter_by_currency_non_currency_code():
    """ Тестирование с пустым или None кодом валюты"""
    transactions = [
        {"operationAmount": {"currency": { "code": "USD"}}},
        {"operationAmount": {"currency": {"code": ""}}}
        ]
    empty_result = list( filter_by_currency(transactions, ""))
    assert empty_result == []

    usd_result = list( filter_by_currency(transactions, "USD"))
    assert len(usd_result) == 1


# Тесты для transaction_description


def test_transaction_description(sample_transaction):
    """ Тест проверяет, что функция возвращает корректные описания для каждой транзакции"""

    description = list(transaction_description(sample_transaction))

    #Проверяем количество описаний (должно быть 5 транзакций)
    assert len(description) == 5

    # Проверяем конкретные описания для каждой транзакции
    assert description[0] == "Перевод организации"
    assert description[1] == "Перевод со счета на счет"
    assert description[2] == "Перевод со счета на счет"
    assert description[3] == "Перевод организации"
    assert description[4] == "Перевод с карты на карту"

    print("\nОписание транзакций")
    for i, desc in enumerate(description, 1):
        print(f"{i}. {desc}")


def test_transaction_description_generator(sample_transaction):
    """ Тестирование использования функции, как генератора"""

    desc_gen = transaction_description(sample_transaction)

    # Получаем описания по одному через next()
    assert next(desc_gen) == "Перевод организации"
    assert next(desc_gen) == "Перевод со счета на счет"
    assert next(desc_gen) == "Перевод со счета на счет"
    assert next(desc_gen) == "Перевод организации"
    assert next(desc_gen) == "Перевод с карты на карту"

    # Больше транзакций нет - должно вызвать StopIteration
    with pytest.raises(StopIteration):
        next(desc_gen)


def test_transaction_description_with_empty_list():
    """
    Тестирование работы функции с пустым списком.
    """
    empty_list = []
    result = list(transaction_description(empty_list))

    # Пустой список должен вернуть пустой список описаний
    assert result == []

    print("\nПустой список транзакций → пустой список описаний")


def test_transaction_description_with_single_transaction():
    """
        Тестирование работы функции с одной транзакцией.
        """
    single_transaction = [
        {
            "id" : 999,
            "description" : "Тестовая транзакция",
            "operationAmount": {"currency": {"code": "USD"}}
    }]
    result = list(transaction_description(single_transaction))

    # Должно вернуть одно описание
    assert len(result) == 1
    assert result[0] == "Тестовая транзакция"

    print(f"\nОдна транзакция → одно описание: {result[0]}")


def test_transaction_description_mix_transaction():
    """ Тестирование работы функции с разным количеством транзакций"""
    # Тест с 0 транзакциями
    result_0 = list(transaction_description([]))
    assert len(result_0) == 0

    # Тест с 1 транзакцией
    result_1 = list(transaction_description([sample_transaction[0]]))
    assert len(result_1) == 1

    # Тест с 3 транзакциями
    result_3 = list(transaction_description(sample_transaction[:3]))
    assert len(result_3) == 3

    # Тест с 5 транзакциями (полная фикстура)
    result_5 = list(transaction_description(sample_transaction))
    assert len(result_5) == 5


# Тесты для card_number_generator

def test_card_number_generator_basic():
    """ Тестирование базовой генерации номеров карт"""
    gen = card_number_generator(1,5)

    #проверяем первые пять номеров
    assert next(gen) == "0000 0000 0000 0001"
    assert next(gen) == "0000 0000 0000 0002"
    assert next(gen) == "0000 0000 0000 0003"
    assert next(gen) == "0000 0000 0000 0004"
    assert next(gen) == "0000 0000 0000 0005"

    # Больше элементов нет
    with pytest.raises(StopIteration):
        next(gen)


def test_card_number_generator_format():
    """Тестирование формата номеров карт"""
    cards = list(card_number_generator(1, 3))

    # Проверяем формат каждой карты
    for card in cards:
        # Должно быть 19 символов (16 цифр + 3 пробела)
        assert len(card) == 19

        # Должно содержать ровно три пробела
        assert card.count(" ") == 3

        # Пробелы должны быть на позициях 4, 9, 14
        assert card[4] == " "
        assert card[9] == " "
        assert card[14] == " "

        # Остальные символы должны быть цифрами
        assert card.replace(" ", "").isdigit()


def test_card_number_generator_edge_cases():
    """Тестирование граничных случаев"""

    # Минимальный номер
    cards = list(card_number_generator(1, 1))
    assert cards[0] == "0000 0000 0000 0001"

    # Максимальный номер
    cards = list(card_number_generator(9999999999999999, 9999999999999999))
    assert cards[0] == "9999 9999 9999 9999"

    # Диапазон из 2 номеров
    cards = list(card_number_generator(9999999999999998, 9999999999999999))
    assert len(cards) == 2
    assert cards[0] == "9999 9999 9999 9998"
    assert cards[1] == "9999 9999 9999 9999"


def test_card_number_generator_invalid_start_greater_than_end():
    """Тестирование ошибки при начальном значении больше конечного"""
    with pytest.raises(ValueError, match="Начальное значение не может быть больше конечного"):
        list(card_number_generator(10, 5))


def test_card_number_generator_invalid_end_too_large():
    """Тестирование ошибки при слишком большом конечном значении"""
    with pytest.raises(ValueError, match="Конечное значение должно быть <= 9999999999999999"):
        list(card_number_generator(1, 10000000000000000))


def test_card_number_generator_invalid_start_too_small():
    """Тестирование ошибки при слишком маленьком начальном значении"""
    with pytest.raises(ValueError, match="Начальное значение должно быть >= 1"):
        list(card_number_generator(0, 5))

