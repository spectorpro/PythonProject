import functools
from typing import Any
from typing import Callable
from typing import Optional


def log(filename: Optional[str] = None) -> Callable:
    """
    Декоратор для логирования начала и конца выполнения функции,
    а также результатов или ошибок.

    Args:
        filename: имя файла для записи логов. Если None, логи выводятся в консоль.
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            func_name: str = func.__name__
            log_message: str = f"{func_name} "

            try:
                result: Any = func(*args, **kwargs)
                log_message += "ok"
                _write_log(log_message, filename)
                return result
            except Exception as e:
                error_type: str = type(e).__name__
                inputs_repr: str = f"Inputs: {args}, {kwargs}"
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
