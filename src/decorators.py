import functools
import traceback
from typing import Any, Callable, Optional

def log(filename: Optional[str] = None) -> Callable:
    """
    Декоратор для логирования начала и конца выполнения функции,
    а также результатов или ошибок.

    Args:
        filename: имя файла для записи логов. Если None, логи выводятся в консоль.
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            func_name = func.__name__
            log_message = f"{func_name} "

            try:
                result = func(*args, **kwargs)
                log_message += "ok"
                _write_log(log_message, filename)
                return result
            except Exception as e:
                error_type = type(e).__name__
                inputs_repr = f"Inputs: {args}, {kwargs}"
                log_message += f"error: {error_type}. {inputs_repr}"
                _write_log(log_message, filename)
                raise
        return wrapper
    return decorator

def _write_log(message: str, filename: Optional[str] = None) -> None:
    """
    Записывает лог-сообщение в файл или выводит в консоль.

    Args:
        message: сообщение для логирования
        filename: имя файла для записи. Если None, выводится в консоль.
    """
    if filename:
        with open(filename, 'a', encoding='utf-8') as f:
            f.write(message + '\n')
    else:
        print(message)
