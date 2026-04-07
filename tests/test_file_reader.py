from unittest.mock import MagicMock, patch

from src.file_reader import _build_nested_structure, read_csv_transactions, read_excel_transactions


@patch("src.file_reader.pd.read_csv")
@patch("src.file_reader.Path.exists")
def test_read_csv_transactions_success(mock_exists, mock_read_csv):
    """Тестирование успешного чтения CSV файла"""
    # Настройка моков
    mock_exists.return_value = True

    # Создаем моки для "строк" DataFrame (имитация pandas.Series)
    mock_row1 = MagicMock()
    mock_row1.to_dict.return_value = {
        "id": "441945886",
        "state": "EXECUTED",
        "date": "2019-08-26T10:50:58.294041",
        "amount": "31957.58",
        "currency_name": "руб.",
        "currency_code": "RUB",
        "description": "Перевод организации",
        "from": "Maestro 1596837868705199",
        "to": "Счет 64686473678894779589",
    }

    mock_row2 = MagicMock()
    mock_row2.to_dict.return_value = {
        "id": "41428829",
        "state": "EXECUTED",
        "date": "2019-07-03T18:35:29.512364",
        "amount": "8221.37",
        "currency_name": "USD",
        "currency_code": "USD",
        "description": "Перевод организации",
        "from": "MasterCard 7158300734726758",
        "to": "Счет 35383033474447895560",
    }

    # Мок для DataFrame
    mock_df = MagicMock()
    mock_df.fillna.return_value = mock_df
    mock_df.iterrows.return_value = [(0, mock_row1), (1, mock_row2)]
    mock_read_csv.return_value = mock_df

    # Вызов функции
    result = read_csv_transactions("transactions.csv")

    # Проверки
    assert len(result) == 2
    assert result[0]["id"] == "441945886"
    assert result[0]["state"] == "EXECUTED"
    assert "operationAmount" in result[0]
    assert result[0]["operationAmount"]["amount"] == "31957.58"
    assert result[0]["operationAmount"]["currency"]["code"] == "RUB"
    assert result[0]["operationAmount"]["currency"]["name"] == "руб."
    assert result[1]["operationAmount"]["currency"]["name"] == "USD"


@patch("src.file_reader.pd.read_csv")
@patch("src.file_reader.Path.exists")
def test_read_csv_transactions_file_not_found(mock_exists, mock_read_csv):
    """Тестирование обработки отсутствующего CSV файла"""
    mock_exists.return_value = False

    result = read_csv_transactions("nonexistent.csv")

    assert result == []
    mock_read_csv.assert_not_called()


@patch("src.file_reader.pd.read_excel")
@patch("src.file_reader.Path.exists")
def test_read_excel_transactions_success(mock_exists, mock_read_excel):
    """Тестирование успешного чтения Excel файла"""
    # Настройка моков
    mock_exists.return_value = True

    # Создаем моки для "строк" Excel
    mock_row1 = MagicMock()
    mock_row1.to_dict.return_value = {
        "id": 441945886,
        "state": "EXECUTED",
        "date": "2019-08-26T10:50:58.294041",
        "amount": "31957.58",
        "currency_name": "руб.",
        "currency_code": "RUB",
        "description": "Перевод организации",
        "from": "Maestro 1596837868705199",
        "to": "Счет 64686473678894779589",
    }

    mock_row2 = MagicMock()
    mock_row2.to_dict.return_value = {
        "id": 41428829,
        "state": "EXECUTED",
        "date": "2019-07-03T18:35:29.512364",
        "amount": "8221.37",
        "currency_name": "USD",
        "currency_code": "USD",
        "description": "Перевод организации",
        "from": "MasterCard 7158300734726758",
        "to": "Счет 35383033474447895560",
    }

    # Мок для DataFrame
    mock_df = MagicMock()
    mock_df.fillna.return_value = mock_df
    mock_df.iterrows.return_value = [(0, mock_row1), (1, mock_row2)]
    mock_read_excel.return_value = mock_df

    # Вызов функции
    result = read_excel_transactions("transactions.xlsx")

    # Проверки
    assert len(result) == 2
    assert result[0]["id"] == 441945886
    assert "operationAmount" in result[0]
    assert result[0]["operationAmount"]["amount"] == "31957.58"
    assert result[1]["operationAmount"]["currency"]["code"] == "USD"


@patch("src.file_reader.pd.read_excel")
@patch("src.file_reader.Path.exists")
def test_read_excel_transactions_empty_file(mock_exists, mock_read_excel):
    """Тестирование обработки пустого Excel файла"""
    mock_exists.return_value = True
    mock_read_excel.side_effect = ValueError("No tables found")

    result = read_excel_transactions("empty.xlsx")

    assert result == []


@patch("src.file_reader.pd.read_csv")
@patch("src.file_reader.Path.exists")
def test_read_csv_transactions_with_spaces_in_keys(mock_exists, mock_read_csv):
    """Тестирование очистки ключей от пробелов в CSV"""
    mock_exists.return_value = True

    # Мок с ключами, содержащими пробелы
    mock_row = MagicMock()
    mock_row.to_dict.return_value = {
        "id ": "441945886",  # Ключ с пробелом
        "state ": "EXECUTED",
        "amount ": "31957.58",
        "currency_code ": "RUB",
    }

    mock_df = MagicMock()
    mock_df.fillna.return_value = mock_df
    mock_df.iterrows.return_value = [(0, mock_row)]
    mock_read_csv.return_value = mock_df

    result = read_csv_transactions("transactions.csv")

    # Ключи должны быть очищены от пробелов
    assert len(result) == 1
    assert "id" in result[0]
    assert "state" in result[0]
    assert result[0]["id"] == "441945886"


def test_build_nested_structure():
    """Тестирование формирования вложенной структуры operationAmount"""
    transaction = {
        "id": "123",
        "amount": "1000.00",
        "currency_name": "USD",
        "currency_code": "USD",
        "description": "Test",
    }

    result = _build_nested_structure(transaction)

    # Проверяем, что поля объединены в operationAmount
    assert "operationAmount" in result
    assert result["operationAmount"]["amount"] == "1000.00"
    assert result["operationAmount"]["currency"]["code"] == "USD"
    assert result["operationAmount"]["currency"]["name"] == "USD"
    # Проверяем, что исходные поля удалены
    assert "amount" not in result
    assert "currency_name" not in result
    assert "currency_code" not in result
    # Проверяем, что другие поля сохранены
    assert result["id"] == "123"
    assert result["description"] == "Test"
