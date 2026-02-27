import pytest
from src.generators import filter_by_currency


"""Фикстура с тестовыми транзакциями"""
@pytest.fixture
def sample_transaction():
    return [
        {
            "id": 1,
            "state": ""
        }
    ]