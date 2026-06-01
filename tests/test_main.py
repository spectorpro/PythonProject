import unittest
from unittest.mock import patch

from main import filter_by_status
from main import filter_ruble_transactions
from main import print_transactions
from main import sort_by_date


class TestBankOperations(unittest.TestCase):

    def setUp(self):
        """Подготовка тестовых данных."""
        self.test_data = [
            {
                'id': 1,
                'date': '01.01.2023',
                'description': 'Покупка в магазине',
                'status': 'EXECUTED',
                'amount': '1000 руб'
            },
            {
                'id': 2,
                'date': '15.02.2023',
                'description': 'Перевод другу',
                'status': 'CANCELED',
                'amount': '500 руб'
            },
            {
                'id': 3,
                'date': '20.03.2023',
                'description': 'Зарплата',
                'status': 'PENDING',
                'amount': '30000 руб'
            },
            {
                'id': 4,
                'date': '10.04.2023',
                'description': 'Оплата услуг',
                'status': 'EXECUTED',
                'amount': '$100'
            }
        ]

    def test_filter_by_status_executed(self):
        """Тест фильтрации по статусу EXECUTED."""
        result = filter_by_status(self.test_data, 'EXECUTED')
        self.assertEqual(len(result), 2)
        self.assertTrue(all(t['status'] == 'EXECUTED' for t in result))

    def test_filter_by_status_canceled(self):
        """Тест фильтрации по статусу CANCELED."""
        result = filter_by_status(self.test_data, 'canceled')  # проверка регистра
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['id'], 2)

    def test_filter_by_status_invalid(self):
        """Тест с некорректным статусом."""
        with self.assertRaises(ValueError) as context:
            filter_by_status(self.test_data, 'INVALID_STATUS')
        self.assertIn('Статус операции', str(context.exception))

    def test_sort_by_date_ascending(self):
        """Тест сортировки по дате (возрастание)."""
        result = sort_by_date(self.test_data, ascending=True)
        dates = [t['date'] for t in result]
        expected_dates = ['01.01.2023', '15.02.2023', '20.03.2023', '10.04.2023']
        self.assertEqual(dates, expected_dates)

    def test_sort_by_date_descending(self):
        """Тест сортировки по дате (убывание)."""
        result = sort_by_date(self.test_data, ascending=False)
        dates = [t['date'] for t in result]
        expected_dates = ['10.04.2023', '20.03.2023', '15.02.2023', '01.01.2023']
        self.assertEqual(dates, expected_dates)

    def test_sort_by_date_invalid_date(self):
        """Тест обработки некорректных дат."""
        data_with_invalid_date = self.test_data.copy()
        data_with_invalid_date[0]['date'] = 'invalid_date'
        result = sort_by_date(data_with_invalid_date, ascending=True)
        # Транзакция с некорректной датой должна быть в начале при возрастающей сортировке
        self.assertEqual(result[0]['id'], 1)

    def test_filter_ruble_transactions(self):
        """Тест фильтрации рублёвых транзакций."""
        result = filter_ruble_transactions(self.test_data)
        self.assertEqual(len(result), 3)
        self.assertFalse(any('$' in str(t.get('amount', '')) for t in result))
        self.assertTrue(all('руб' in str(t.get('amount', '')).lower() for t in result))

    def test_filter_ruble_transactions_no_ruble(self):
        """Тест когда нет рублёвых транзакций."""
        data_no_rub = [
            {'date': '01.01.2023', 'description': 'USD transfer', 'amount': '$100'},
            {'date': '02.01.2023', 'description': 'EUR transfer', 'amount': '€50'}
        ]
        result = filter_ruble_transactions(data_no_rub)
        self.assertEqual(len(result), 0)

    @patch('builtins.print')
    def test_print_transactions_with_data(self, mock_print):
        """Тест вывода транзакций с данными."""
        print_transactions(self.test_data[:2])
        calls = mock_print.call_args_list
        self.assertGreater(len(calls), 2)  # Должен быть заголовок и 2 транзакции
        self.assertIn('Всего банковских операций в выборке: 2', str(calls[0]))
        self.assertIn('01.01.2023 Покупка в магазине Сумма: 1000 руб', str(calls[1]))

    @patch('builtins.print')
    def test_print_transactions_empty(self, mock_print):
        """Тест вывода пустого списка транзакций."""
        print_transactions([])
        mock_print.assert_called_once_with("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")

    def test_edge_cases(self):
        """Тест крайних случаев."""
        # Пустой список
        self.assertEqual(filter_by_status([], 'EXECUTED'), [])
        self.assertEqual(sort_by_date([], True), [])
        self.assertEqual(filter_ruble_transactions([]), [])

        # Транзакции без поля status
        data_without_status = [{'id': 1, 'date': '01.01.2023'}]
        result = filter_by_status(data_without_status, 'EXECUTED')
        self.assertEqual(len(result), 0)

        # Транзакции без поля amount
        data_without_amount = [{'id': 1, 'date': '01.01.2023', 'status': 'EXECUTED'}]
        result = filter_ruble_transactions(data_without_amount)
        self.assertEqual(len(result), 0)


if __name__ == '__main__':
    unittest.main()
