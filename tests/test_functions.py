import unittest
from unittest.mock import patch, mock_open
from utils import load_transactions
from external_api import convert_to_rubles


class TestUtils(unittest.TestCase):

    @patch('os.path.exists', return_value=False)
    def test_load_transactions_file_not_found(self, mock_exists):
        result = load_transactions('non_existent_file.json')
        self.assertEqual(result, [])

    @patch('builtins.open', mock_open(read_data='{"not": "a list"}'))
    @patch('os.path.exists', return_value=True)
    def test_load_transactions_not_a_list(self, mock_exists, mock_file):
        result = load_transactions('test.json')
        self.assertEqual(result, [])

    @patch('builtins.open', mock_open(read_data='[{"id": 1, "amount": 100}]'))
    @patch('os.path.exists', return_value=True)
    def test_load_transactions_valid_data(self, mock_exists, mock_file):
        result = load_transactions('test.json')
        expected = [{"id": 1, "amount": 100}]
        self.assertEqual(result, expected)

    @patch('builtins.open', mock_open(read_data='invalid json'))
    @patch('os.path.exists', return_value=True)
    def test_load_transactions_invalid_json(self, mock_exists, mock_file):
        result = load_transactions('test.json')
        self.assertEqual(result, [])

class TestExternalAPI(unittest.TestCase):

    @patch('external_api.get_exchange_rate', return_value=75.0)
    def test_convert_to_rubles_usd(self, mock_get_rate):
        transaction = {'amount': 10, 'currency': 'USD'}
        result = convert_to_rubles(transaction)
        self.assertAlmostEqual(result, 750.0)

    @patch('external_api.get_exchange_rate', return_value=85.0)
    def test_convert_to_rubles_eur(self, mock_get_rate):
        transaction = {'amount': 5, 'currency': 'EUR'}
        result = convert_to_rubles(transaction)
        self.assertAlmostEqual(result, 425.0)

    def test_convert_to_rubles_rub(self):
        transaction = {'amount': 1000, 'currency': 'RUB'}
        result = convert_to_rubles(transaction)
        self.assertEqual(result, 1000.0)

    @patch('external_api.get_exchange_rate', return_value=None)
    def test_convert_to_rubles_api_error(self, mock_get_rate):
        transaction = {'amount': 10, 'currency': 'USD'}
        with self.assertRaises(ValueError):
            convert_to_rubles(transaction)

if __name__ == '__main__':
    unittest.main()
