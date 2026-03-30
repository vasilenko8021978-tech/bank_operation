from .logger import setup_logger

# Создаём отдельный объект логера для модуля masks
logger = setup_logger(__name__, log_file="masks")


def get_mask_card_number(card_number: str) -> str:
    """
    Маскирует номер карты.

    :param card_number: Номер карты
    :return: Замаскированный номер карты или сообщение об ошибке
    """
    try:
        logger.debug(f"Начата маскировка номера карты: {card_number}")

        # Убираем пробелы
        cleaned_number = card_number.replace(" ", "")

        # Проверяем пустую строку
        if not cleaned_number:
            logger.error(f"Отсутствует номер карты: {card_number}")
            return "отсутствует номер карты"

        # Проверяем, что номер содержит только цифры
        if not cleaned_number.isdigit():
            logger.error(f"Номер карты содержит нецифровые символы: {card_number}")
            return "номер должен быть только из цифр"

        # Проверяем длину номера
        if len(cleaned_number) != 16:
            logger.error(f"Неверная длина номера карты: {len(cleaned_number)}")
            return "количество цифр не равно 16"

        # Маскируем номер (показываем первые 4 и последние 4 цифры)
        masked = f"{cleaned_number[:4]} {cleaned_number[4:6]}** **** {cleaned_number[-4:]}"

        logger.info(f"Маскировка успешна: {masked}")
        return masked

    except Exception as e:
        logger.error(f"Ошибка при маскировке номера карты: {e}", exc_info=True)
        return "Ошибка при маскировке номера карты"


def get_mask_account(account_number: str) -> str:
    """
    Маскирует номер счёта.

    :param account_number: Номер счёта
    :return: Замаскированный номер счёта или сообщение об ошибке
    """
    try:
        logger.debug(f"Начата маскировка номера счёта: {account_number}")

        # Убираем пробелы
        cleaned_number = account_number.replace(" ", "")

        # Проверяем пустую строку
        if not cleaned_number:
            logger.error(f"Отсутствует номер счёта: {account_number}")
            return "отсутствует номер карты"

        # Проверяем, что номер содержит только цифры
        if not cleaned_number.isdigit():
            logger.error(f"Номер счёта содержит нецифровые символы: {account_number}")
            return "номер должен быть только из цифр"

        # Проверяем длину номера (для счёта должно быть 20 цифр)
        if len(cleaned_number) != 20:
            logger.error(f"Неверная длина номера счёта: {len(cleaned_number)}")
            return "количество цифр не равно 20"

        # Маскируем номер (показываем последние 4 цифры)
        masked = f"**{cleaned_number[-4:]}"

        logger.info(f"Маскировка успешна: {masked}")
        return masked

    except Exception as e:
        logger.error(f"Ошибка при маскировке номера счёта: {e}", exc_info=True)
        return "Ошибка при маскировке номера счёта"
