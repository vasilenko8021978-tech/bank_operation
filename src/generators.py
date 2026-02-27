from typing import List, Dict, Any, Iterator, Tuple


def filter_by_currency(transactions: List[Dict[str, Any]],currency_code: str) -> Iterator[Dict[str, Any]]:
    """ Функция, принимает на вход список словарей, представляющих транзакции
    и возвращает итератор, который поочередно выдает транзакции, где валюта
    операции соответствует заданной"""
    for transaction in transactions:
        try:
            if ("operationAmont" in transaction and "currency" in transaction["operationAmont"] and transaction["operationAmont"]
                    and "code" in transaction["operationAmont"]["currency"]):
                if transaction["operationAmont"]["currency"]["code"].upper == currency_code.upper():
                    yield transaction
        except (KeyError, TypeError):
            continue