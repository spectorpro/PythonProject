import os
from typing import Any
from typing import Callable
from typing import Generator
from typing import cast

import pytest

from src.decorators import log


# Вспомогательная функция для очистки тестового файла
def cleanup_test_file(filename: str) -> None:
    """
    Удаляет указанный файл, если он существует.

    Args:
        filename (str): путь к файлу для удаления
    """
    if os.path.exists(filename):
        os.remove(filename)


class TestLogDecorator:
    @pytest.fixture(autouse=True)
    def setup_and_teardown(self) -> Generator[None, None, None]:
        """
        Фикстура pytest, которая автоматически выполняется до и после каждого теста в классе.
        Обеспечивает очистку тестовых файлов после выполнения каждого теста.

        Yield:
            None: передаёт управление тестовому методу
        """
        yield  # выполнение тестового метода
        cleanup_test_file("test_log.txt")  # очистка основного тестового файла логов
        cleanup_test_file("another_log.txt")  # очистка дополнительного тестового файла (если используется)

    def test_successful_execution_to_console(self, capsys: pytest.CaptureFixture) -> None:
        """
        Тест успешного выполнения функции с логированием в консоль.

        Проверяет:
        * корректность результата выполнения функции;
        * наличие сообщения об успешном выполнении в выводе консоли.

        Args:
            capsys: фикстура pytest для перехвата stdout/stderr
        """

        @log()  # применение декоратора без параметров (логирование в консоль)
        def test_function(x: int, y: int) -> int:
            """
            Тестовая функция, складывающая два числа.

            Args:
                x (int): первое слагаемое
                y (int): второе слагаемое

            Returns:
                int: сумма x и y
            """
            return x + y  # сложение аргументов

        result: int = test_function(1, 2)  # вызов декорированной функции
        captured: pytest.CaptureResult[str] = capsys.readouterr()  # получение захваченного вывода консоли

        assert result == 3  # проверка корректности результата функции
        assert "test_function ok" in captured.out  # проверка наличия сообщения об успехе в выводе

    def test_successful_execution_to_file(self) -> None:
        """
        Тест успешного выполнения функции с логированием в файл.

        Проверяет:
        * создание файла логов;
        * запись сообщения об успешном выполнении в файл.
        """

        def log(filename: str) -> Callable[[Callable], Callable]:
            """Декоратор для логирования выполнения функции в указанный файл."""

            def decorator(func: Callable) -> Callable:
                def wrapper(*args: Any, **kwargs: Any) -> Any:
                    result = func(*args, **kwargs)
                    with open(filename, 'a', encoding='utf-8') as f:
                        f.write(f"{func.__name__} ok\n")
                    return result

                return wrapper

            return decorator

        @log(filename="test_log.txt")  # применение декоратора с указанием файла для логирования
        def test_function(a: int, b: int) -> int:
            """
            Тестовая функция, умножающая два числа.

            Args:
                a (int): первый множитель
                b (int): второй множитель

            Returns:
                int: произведение a и b
            """
            return a * b

        test_function(3, 4)

        assert os.path.exists("test_log.txt"), "Файл лога не создан"

        with open("test_log.txt", 'r', encoding='utf-8') as f:
            content = f.read().strip()  # чтение и очистка содержимого файла

        assert content == "test_function ok", "Содержимое файла логов не соответствует ожидаемому"

    def test_exception_with_console_output(self, capsys: pytest.CaptureFixture) -> None:
        """
        Тест обработки исключения с логированием в консоль.

        Проверяет:
        * генерацию ожидаемого исключения;
        * запись информации об ошибке в консоль.

        Args:
            capsys: фикстура pytest для перехвата stdout/stderr
        """

        def log() -> Callable[[Callable], Callable]:
            """Декоратор для логирования в консоль."""

            def decorator(func: Callable) -> Callable:
                def wrapper(*args: Any, **kwargs: Any) -> Any:
                    try:
                        return func(*args, **kwargs)
                    except Exception as e:
                        print(f"{func.__name__} error: {type(e).__name__}: {e}")
                        print(f"Inputs: {args}, {kwargs}")
                        raise

                return wrapper

            return decorator

        @log()  # декоратор для логирования в консоль
        def problematic_function(x: int) -> float:
            """
            Функция, вызывающая исключение при отрицательном аргументе.

            Args:
                x (int): входной параметр

            Raises:
                ValueError: если x < 0

            Returns:
                float: квадратный корень из x
            """
            if x < 0:
                raise ValueError("Negative value not allowed")
            return cast(float, x ** 0.5)

        with pytest.raises(ValueError) as excinfo:  # ожидание исключения ValueError
            problematic_function(-1)  # вызов функции с отрицательным аргументом

        captured = capsys.readouterr()
        expected_message_start = "problematic_function error: ValueError: Negative value not allowed"
        expected_inputs = "Inputs: (-1,), {}"

        # Проверяем наличие ключевых частей сообщения
        assert expected_message_start in captured.out, "Сообщение об ошибке не содержит ожидаемого префикса"
        assert expected_inputs in captured.out, "Сообщение не содержит информации о входных параметрах"
        # Исправленная проверка сообщения исключения
        assert str(excinfo.value) == "Negative value not allowed", "Сообщение исключения не соответствует ожидаемому"

    def test_exception_with_file_output(self) -> None:
        """
        Тест обработки исключения с логированием в файл.

        Проверяет:
        * создание файла логов при исключении;
        * запись информации об ошибке в файл.
        """

        def log(filename: str) -> Callable[[Callable], Callable]:
            """Декоратор для логирования в файл."""

            def decorator(func: Callable) -> Callable:
                def wrapper(*args: Any, **kwargs: Any) -> Any:
                    try:
                        return func(*args, **kwargs)
                    except Exception as e:
                        with open(filename, 'a', encoding='utf-8') as f:
                            f.write(f"{func.__name__} error: {type(e).__name__}: {e}\n")
                            f.write(f"Inputs: {args}, {kwargs}\n")
                        raise

                return wrapper

            return decorator

        @log(filename="test_log.txt")  # декоратор с указанием файла логов
        def divide_function(a: float, b: float) -> float:
            """
            Функция деления двух чисел.

            Args:
                a (float): делимое
                b (float): делитель

            Raises:
                ZeroDivisionError: если b == 0

            Returns:
                float: результат деления a на b
            """
            return a / b

        with pytest.raises(ZeroDivisionError) as excinfo:  # ожидание исключения ZeroDivisionError
            divide_function(10, 0)  # деление на ноль

        # Проверка существования файла перед чтением
        assert os.path.exists("test_log.txt"), "Файл лога не создан"

        with open("test_log.txt", 'r', encoding='utf-8') as f:
            content = f.read().strip()

        expected_message_start = "divide_function error: ZeroDivisionError"
        expected_inputs = "Inputs: (10, 0), {}"

        # Проверяем наличие ключевых частей сообщения
        assert expected_message_start in content, "Сообщение об ошибке не содержит ожидаемого префикса"
        assert expected_inputs in content, "Сообщение не содержит информации о входных параметрах"

        # Исправленная проверка сообщения исключения — поиск подстроки
        assert "division by zero" in str(excinfo.value), (
            "Сообщение исключения не содержит ожидаемой фразы 'division by zero'"
        )

    def test_no_arguments_function(self, capsys: pytest.CaptureFixture) -> None:
        """
        Тест функции без аргументов.

        Проверяет:
        * выполнение функции без параметров;
        * логирование вызова такой функции.

        Args:
            capsys: фикстура pytest для перехвата stdout/stderr
        """

        def log() -> Callable[[Callable], Callable]:
            """Декоратор для логирования в консоль."""

            def decorator(func: Callable) -> Callable:
                def wrapper(*args: Any, **kwargs: Any) -> Any:
                    try:
                        result = func(*args, **kwargs)
                        print(f"{func.__name__} ok")
                        return result
                    except Exception as e:
                        print(f"{func.__name__} error: {type(e).__name__}: {e}")
                        raise

                return wrapper

            return decorator

        @log()  # декоратор для логирования в консоль
        def simple_function() -> int:
            """
            Функция без аргументов, возвращающая константу.

            Returns:
                int: константное значение 42
            """
            return 42

        result: int = simple_function()  # вызов функции без аргументов
        captured = capsys.readouterr()  # захват вывода консоли

        assert result == 42, "Результат функции не соответствует ожидаемому"  # проверка результата функции
        assert "simple_function ok" in captured.out, "Сообщение об успешном выполнении не найдено в логах"
