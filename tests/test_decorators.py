import os
import pytest
from src.decorators import log

# Вспомогательная функция для очистки тестового файла
def cleanup_test_file(filename: str) -> None:
    if os.path.exists(filename):
        os.remove(filename)

class TestLogDecorator:
    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        """Очистка тестовых файлов после каждого теста"""
        yield
        cleanup_test_file("test_log.txt")
        cleanup_test_file("another_log.txt")

    def test_successful_execution_to_console(self, capsys):
        """Тест успешного выполнения функции с логированием в консоль"""
        @log()
        def test_function(x, y):
            return x + y

        result = test_function(1, 2)
        captured = capsys.readouterr()

        assert result == 3
        assert "test_function ok" in captured.out

    def test_successful_execution_to_file(self):
        """Тест успешного выполнения функции с логированием в файл"""
        @log(filename="test_log.txt")
        def test_function(a, b):
            return a * b

        test_function(3, 4)

        with open("test_log.txt", 'r', encoding='utf-8') as f:
            content = f.read().strip()

        assert content == "test_function ok"

    def test_exception_with_console_output(self, capsys):
        """Тест обработки исключения с логированием в консоль"""
        @log()
        def problematic_function(x):
            if x < 0:
                raise ValueError("Negative value not allowed")
            return x ** 0.5

        with pytest.raises(ValueError):
            problematic_function(-1)

        captured = capsys.readouterr()
        expected_message = "problematic_function error: ValueError. Inputs: (-1,), {}"
        assert expected_message in captured.out

    def test_exception_with_file_output(self):
        """Тест обработки исключения с логированием в файл"""
        @log(filename="test_log.txt")
        def divide_function(a, b):
            return a / b

        with pytest.raises(ZeroDivisionError):
            divide_function(10, 0)

        with open("test_log.txt", 'r', encoding='utf-8') as f:
            content = f.read().strip()

        expected_message = "divide_function error: ZeroDivisionError. Inputs: (10, 0), {}"
        assert content == expected_message



    def test_no_arguments_function(self, capsys):
        """Тест функции без аргументов"""
        @log()
        def simple_function():
            return 42

        result = simple_function()
        captured = capsys.readouterr()

        assert result == 42
        assert "simple_function ok" in captured.out
