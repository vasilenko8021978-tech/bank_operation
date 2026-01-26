def get_mask_card_number(number: str) -> str:
    """
    Преобразование числа в маску
    :param number: данный параметр принимает целочисленный тип данных
    :return: строку в формате ХХХХ ХХ** **** ХХХХ
    """
    res_l = []
    conv_str = number
    count_stars = "*" * (len(conv_str) - 10)
    split_number = f"{conv_str[:6]}{count_stars}{conv_str[-4:]}"
    for i in range(0, len(split_number), 4):
        res_l.append(split_number[i : i + 4])
    return " ".join(res_l)


def get_mask_account(number: str) -> str:
    """
    Преобразование числа в маску счета
    :param number: данный параметр принимает целочисленный тип данных
    :return: строку в формате **ХХХХ
    """
    conv_str = number
    return f"**{conv_str[-4:]}"
