from datetime import datetime
from functools import wraps
from typing import Any, Callable, Optional


def log(filename: Optional[str] = None) -> Callable:
    """
    Декоратор для автоматического логирования выполнения функции.

    :param filename: Имя файла для записи логов. Если не указано, логи выводятся в консоль.
    :return: Декорированная функция
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Получаем текущее время
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            try:
                # Выполнение функции
                result = func(*args, **kwargs)

                # Формирование сообщения об успешном выполнении с временем
                log_message = f"[{timestamp}] {func.__name__} ok"

                # Запись лога
                if filename:
                    with open(filename, "a", encoding="utf-8") as f:
                        f.write(log_message + "\n")
                else:
                    print(log_message)

                return result

            except Exception as e:
                # Формирование сообщения об ошибке с временем
                error_type = type(e).__name__
                log_message = f"[{timestamp}] {func.__name__} error: {error_type}. Inputs: {args}, {kwargs}"

                # Запись лога
                if filename:
                    with open(filename, "a", encoding="utf-8") as f:
                        f.write(log_message + "\n")
                else:
                    print(log_message)

                # Пробрасываем исключение дальше
                raise

        return wrapper

    return decorator
