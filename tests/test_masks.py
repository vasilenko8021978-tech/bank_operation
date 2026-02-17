import pytest

from src.masks import get_mask_account, get_mask_card_number


@pytest.mark.parametrize(
    "x, y",
    [
        ("2345 3345 7766 1122", "2345 33** **** 1122"),
        ("421223483456228796", "количество цифр не равно 16"),
        ("123a 1234 3421 2341", "номер должен быть только из цифр"),
        (" ", "отсутствует номер карты"),
    ],
)
def test_get_mask_card_number(x: str, y: str) -> None:
    assert get_mask_card_number(x) == y


@pytest.mark.parametrize(
    "d,f",
    [
        ("2233 2345 4576 7788 2233", "**2233"),
        ("2222 3344 44444 5555 88888", "количество цифр не равно 20"),
        ("222f jjjj 3333 2233 7777", "номер должен быть только из цифр"),
        (" ", "отсутствует номер счета"),
    ],
)
def test_get_mask_account(d: str, f: str) -> None:
    assert get_mask_account(d) == f
