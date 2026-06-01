import unittest

from src.bank_operations import process_bank_operations
from src.bank_operations import process_bank_search


class TestProcessBankSearch(unittest.TestCase):

    def setUp(self):
        """Подготавливаем тестовые данные перед каждым тестом."""
        self.test_data = [
            {'id': 1, 'description': 'Покупка в магазине Пятерочка', 'amount': 1500},
            {'id': 2, 'description': 'Оплата интернета', 'amount': 500},
            {'id': 3, 'description': 'Перевод другу', 'amount': 2000},
            {'id': 4, 'description': 'Списание за обслуживание карты', 'amount': 99},
            {'id': 5, 'description': 'Возврат от Пятерочки', 'amount': -1500}
        ]

    def test_case_insensitive(self):
        """Тест нечувствительности к регистру."""
        result = process_bank_search(self.test_data, 'пятерочка')
        self.assertEqual(len(result), 1)

    def test_partial_match(self):
        """Тест частичного совпадения."""
        result = process_bank_search(self.test_data, 'оплата')
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['id'], 2)

    def test_no_matches(self):
        """Тест отсутствия совпадений."""
        result = process_bank_search(self.test_data, 'не существующая строка')
        self.assertEqual(len(result), 0)

    def test_empty_search_string(self):
        """Тест пустой строки поиска."""
        result = process_bank_search(self.test_data, '')
        self.assertEqual(len(result), len(self.test_data))

    def test_empty_data(self):
        """Тест с пустым списком данных."""
        result = process_bank_search([], 'Пятерочка')
        self.assertEqual(len(result), 0)

    def test_description_missing(self):
        """Тест когда поле description отсутствует."""
        data_with_missing_desc = self.test_data + [{'id': 6, 'amount': 100}]
        result = process_bank_search(data_with_missing_desc, 'Пятерочка')
        self.assertEqual(len(result), 1)


class TestProcessBankOperations(unittest.TestCase):

    def setUp(self):
        """Подготавливаем тестовые данные перед каждым тестом."""
        self.test_data = [
            {'id': 1, 'description': 'Покупка в магазине Пятерочка продукты', 'amount': 1500},
            {'id': 2, 'description': 'Оплата домашнего интернета МТС', 'amount': 500},
            {'id': 3, 'description': 'Перевод другу на день рождения', 'amount': 2000},
            {'id': 4, 'description': 'Списание за обслуживание банковской карты', 'amount': 99},
            {'id': 5, 'description': 'Возврат от Пятерочки за некачественный товар', 'amount': -1500},
            {'id': 6, 'description': 'Пополнение счета через терминал', 'amount': 5000},
            {'id': 7, 'description': 'Оплата мобильной связи Билайн', 'amount': 300}
        ]
        self.categories = ['продукты', 'интернет', 'перевод', 'обслуживание', 'возврат', 'пополнение']

    def test_basic_counting(self):
        """Базовый тест подсчёта операций по категориям."""
        result = process_bank_operations(self.test_data, self.categories)
        expected = {
            'продукты': 1,
            'интернет': 1,
            'перевод': 1,
            'обслуживание': 1,
            'возврат': 1,
            'пополнение': 1,
        }
        self.assertEqual(result, expected)

    def test_case_insensitivity(self):
        """Тест нечувствительности к регистру при поиске категорий."""
        result = process_bank_operations(self.test_data, ['Продукты', 'Интернет'])
        self.assertEqual(result['Продукты'], 1)
        self.assertEqual(result['Интернет'], 1)

    def test_category_not_found(self):
        """Тест когда категория не найдена ни в одной транзакции."""
        categories_with_missing = self.categories + ['не существующая категория']
        result = process_bank_operations(self.test_data, categories_with_missing)
        self.assertEqual(result['не существующая категория'], 0)

    def test_empty_data(self):
        """Тест с пустым списком данных."""
        result = process_bank_operations([], self.categories)
        expected = {category: 0 for category in self.categories}
        self.assertEqual(result, expected)

    def test_empty_categories(self):
        """Тест с пустым списком категорий."""
        result = process_bank_operations(self.test_data, [])
        self.assertEqual(result, {})

    def test_partial_category_match(self):
        """Тест частичного совпадения категорий."""
        # Категория 'продукт' должна найти 'продукты'
        result = process_bank_operations(self.test_data, ['продукт'])
        self.assertEqual(result['продукт'], 1)


if __name__ == '__main__':
    unittest.main()
