from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(number: str) -> str:
    """Функция, которая умеет обрабатывать информацию как о картах, так и о счетах."""

    if "счет" in number.lower():
        return f"Cчет {get_mask_account(number.split()[-1])}"
    else:
        card_name = " ".join(number.split()[:-1])
        card_mask = get_mask_card_number(number.split()[-1])

    return f"{card_name} {card_mask}"


def get_date(date: str) -> str:
    """принимает на вход строку с датой в формате
    "2024-03-11T02:26:18.671407"
     и возвращает строку с датой в формате
    "ДД.ММ.ГГГГ"
     (
    "11.03.2024"
    )"""
    conv_date = date[8:10] + "." + date[5:7] + "." + date[:4]
    return conv_date


if __name__ == "__main__":
    print(get_date("2024-03-11T02:26:18.671407"))
