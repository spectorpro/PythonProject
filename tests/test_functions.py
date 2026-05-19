import unittest
from typing import Dict
from unittest.mock import mock_open
from unittest.mock import patch

from src.external_api import convert_to_rubles
from src.utils import load_transactions


class TestUtils(unittest.TestCase):

    def test_load_transactions_file_not_found(self) -> None:
        with patch('os.path.exists', return_value=False):
            result = load_transactions('non_existent_file.json')
            self.assertEqual(result, [])

    def test_load_transactions_not_a_file(self) -> None:
        with patch('os.path.exists', return_value=True), \
             patch('os.path.isfile', return_value=False):
            result = load_transactions('some_directory')
            self.assertEqual(result, [])

    def test_load_transactions_not_a_list(self) -> None:
        with patch('os.path.exists', return_value=True), \
             patch('os.path.isfile', return_value=True), \
             patch('builtins.open', mock_open(read_data='{"not": "a list"}')):
            result = load_transactions('test.json')
            self.assertEqual(result, [])

    def test_load_transactions_valid_data(self) -> None:
        with patch('os.path.exists', return_value=True), \
             patch('os.path.isfile', return_value=True), \
             patch('builtins.open', mock_open(read_data='[{"id": 1, "amount": 100}]')):
            result = load_transactions('test.json')
            expected: list[Dict] = [{"id": 1, "amount": 100}]
            self.assertEqual(result, expected)

    def test_load_transactions_invalid_json(self) -> None:
        with patch('os.path.exists', return_value=True), \
             patch('os.path.isfile', return_value=True), \
             patch('builtins.open', mock_open(read_data='invalid json')):
            result = load_transactions('test.json')
            self.assertEqual(result, [])


class TestExternalAPI(unittest.TestCase):

    @patch('src.external_api.get_exchange_rate', return_value=75.0)
    def test_convert_to_rubles_usd(self, mock_get_rate: unittest.mock.Mock) -> None:
        transaction: Dict = {'amount': 10, 'currency': 'USD'}
        result = convert_to_rubles(transaction)
        self.assertAlmostEqual(result, 750.0)

    @patch('src.external_api.get_exchange_rate', return_value=85.0)
    def test_convert_to_rubles_eur(self, mock_get_rate: unittest.mock.Mock) -> None:
        transaction: Dict = {'amount': 5, 'currency': 'EUR'}
        result = convert_to_rubles(transaction)
        self.assertAlmostEqual(result, 425.0)

    def test_convert_to_rubles_rub(self) -> None:
        transaction: Dict = {'amount': 1000, 'currency': 'RUB'}
        result = convert_to_rubles(transaction)
        self.assertEqual(result, 1000.0)

    @patch('src.external_api.get_exchange_rate', return_value=None)
    def test_convert_to_rubles_api_error(self, mock_get_rate: unittest.mock.Mock) -> None:
        transaction: Dict = {'amount': 10, 'currency': 'USD'}
        with self.assertRaises(ValueError):
            convert_to_rubles(transaction)


if __name__ == '__main__':
    unittest.main()
