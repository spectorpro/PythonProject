import json
import os
import unittest

import pandas as pd

from src.data_loaders import load_csv_data
from src.data_loaders import load_json_data
from src.data_loaders import load_xlsx_data


class TestDataLoaders(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Создаём тестовые файлы перед запуском всех тестов"""
        # JSON файл
        cls.test_json_content = [
            {"id": 1, "name": "Alice", "age": 25},
            {"id": 2, "name": "Bob", "age": 30}
        ]
        with open('test_data.json', 'w', encoding='utf-8') as f:
            json.dump(cls.test_json_content, f)

        # CSV файл
        cls.test_csv_content = '''id,name,age
1,Alice,25
2,Bob,30'''
        with open('test_data.csv', 'w', encoding='utf-8') as f:
            f.write(cls.test_csv_content)

        # XLSX файл
        df = pd.DataFrame(cls.test_json_content)
        df.to_excel('test_data.xlsx', index=False)

    @classmethod
    def tearDownClass(cls):
        """Удаляем тестовые файлы после завершения всех тестов"""
        for file in ['test_data.json', 'test_data.csv', 'test_data.xlsx']:
            if os.path.exists(file):
                os.remove(file)

    def test_load_json_data_success(self):
        """Тест успешной загрузки JSON файла"""
        result = load_json_data('test_data.json')
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result, list)
        self.assertIsInstance(result[0], dict)
        self.assertEqual(result[0]['name'], 'Alice')
        self.assertEqual(result[1]['age'], 30)

    def test_load_json_data_file_not_found(self):
        """Тест обработки ошибки отсутствия JSON файла"""
        with self.assertRaises(FileNotFoundError):
            load_json_data('nonexistent.json')

    def test_load_json_data_invalid_json(self):
        """Тест обработки некорректного JSON"""
        # Создаём файл с некорректным JSON
        with open('invalid.json', 'w', encoding='utf-8') as f:
            f.write('{invalid json}')

        with self.assertRaises(json.JSONDecodeError):
            load_json_data('invalid.json')

        os.remove('invalid.json')

    def test_load_csv_data_success(self):
        """Тест успешной загрузки CSV файла"""
        result = load_csv_data('test_data.csv')
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result, list)
        self.assertIsInstance(result[0], dict)
        self.assertEqual(result[0]['name'], 'Alice')
        self.assertEqual(result[1]['age'], '30')  # В CSV числа как строки

    def test_load_csv_data_file_not_found(self):
        """Тест обработки ошибки отсутствия CSV файла"""
        with self.assertRaises(FileNotFoundError):
            load_csv_data('nonexistent.csv')

    def test_load_csv_data_empty_file(self):
        """Тест загрузки пустого CSV файла"""
        with open('empty.csv', 'w', encoding='utf-8'):
            pass  # Пустой файл

        result = load_csv_data('empty.csv')
        self.assertEqual(len(result), 0)
        os.remove('empty.csv')

    def test_load_csv_data_with_headers_only(self):
        """Тест CSV файла только с заголовками"""
        content = 'id,name,age'
        with open('headers_only.csv', 'w', encoding='utf-8') as f:
            f.write(content)

        result = load_csv_data('headers_only.csv')
        self.assertEqual(len(result), 0)
        os.remove('headers_only.csv')

    def test_load_xlsx_data_success(self):
        """Тест успешной загрузки XLSX файла"""
        result = load_xlsx_data('test_data.xlsx')
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result, list)
        self.assertIsInstance(result[0], dict)
        self.assertEqual(result[0]['name'], 'Alice')
        self.assertEqual(result[1]['age'], 30)  # В XLSX числа сохраняются как числа

    def test_load_xlsx_data_file_not_found(self):
        """Тест обработки ошибки отсутствия XLSX файла"""
        with self.assertRaises(FileNotFoundError):
            load_xlsx_data('nonexistent.xlsx')

    def test_load_xlsx_data_empty_sheet(self):
        """Тест XLSX файла с пустым листом"""
        empty_df = pd.DataFrame()
        empty_df.to_excel('empty_sheet.xlsx', index=False)

        result = load_xlsx_data('empty_sheet.xlsx')
        self.assertEqual(len(result), 0)
        os.remove('empty_sheet.xlsx')

    def test_load_xlsx_data_single_row(self):
        """Тест XLSX с одной строкой данных"""
        single_row = pd.DataFrame([{'id': 99, 'name': 'Charlie', 'age': 35}])
        single_row.to_excel('single_row.xlsx', index=False)

        result = load_xlsx_data('single_row.xlsx')
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['name'], 'Charlie')
        os.remove('single_row.xlsx')


if __name__ == '__main__':
    unittest.main()
