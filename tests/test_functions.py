import os
from unittest.mock import Mock
from unittest.mock import patch

import pytest
import requests

from src.external_api import convert_to_rubles
from src.external_api import get_exchange_rate


class TestGetExchangeRate:
    @patch('requests.get')
    def test_success_response(self, mock_get):
        """Тест успешного получения курса"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "success": True,
            "rates": {"RUB": 90.5}
        }
        mock_get.return_value = mock_response

        with patch.dict(os.environ, {'API_KEY': 'test_key'}):
            result = get_exchange_rate("USD")
            assert result == 90.5

    @patch('requests.get')
    def test_api_key_missing(self, mock_get):
        """Тест отсутствия API-ключа"""
        result = get_exchange_rate("USD")
        assert result is None

    @patch('requests.get')
    def test_unauthorized(self, mock_get):
        """Тест ошибки аутентификации (401)"""
        mock_response = Mock()
        mock_response.status_code = 401
        mock_get.return_value = mock_response

        with patch.dict(os.environ, {'API_KEY': 'test_key'}):
            result = get_exchange_rate("USD")
            assert result is None

    @patch('requests.get')
    def test_rate_not_found(self, mock_get):
        """Тест когда курс не найден в ответе API"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "success": True,
            "rates": {}
        }
        mock_get.return_value = mock_response

        with patch.dict(os.environ, {'API_KEY': 'test_key'}):
            result = get_exchange_rate("USD")
            assert result is None

    @patch('requests.get')
    def test_api_error_response(self, mock_get):
        """Тест ответа API с ошибкой"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "success": False,
            "error": {"info": "Test error"}
        }
        mock_get.return_value = mock_response

        with patch.dict(os.environ, {'API_KEY': 'test_key'}):
            result = get_exchange_rate("USD")
            assert result is None

    @patch('requests.get')
    def test_timeout_error(self, mock_get):
        """Тест ошибки таймаута"""
        mock_get.side_effect = requests.exceptions.Timeout

        with patch.dict(os.environ, {'API_KEY': 'test_key'}):
            result = get_exchange_rate("USD")
            assert result is None


class TestConvertToRubles:
    def test_convert_usd_to_rub(self):
        """Конвертация USD в RUB с успешным получением курса"""
        transaction = {"amount": 100, "currency": "USD"}

        with patch('src.external_api.get_exchange_rate', return_value=90.5):
            result = convert_to_rubles(transaction)
            assert result == 9050.0

    def test_already_in_rub(self):
        """Транзакция уже в рублях"""
        transaction = {"amount": 5000, "currency": "RUB"}
        result = convert_to_rubles(transaction)
        assert result == 5000.0

    def test_invalid_transaction_type(self):
        """Некорректный тип транзакции"""
        with pytest.raises(ValueError, match="Транзакция должна быть словарем"):
            convert_to_rubles("not a dict")

    def test_missing_amount(self):
        """Отсутствие поля amount"""
        transaction = {"currency": "USD"}
        with pytest.raises(ValueError, match="Транзакция не содержит поле 'amount'"):
            convert_to_rubles(transaction)

    def test_missing_currency(self):
        """Отсутствие поля currency"""
        transaction = {"amount": 100}
        with pytest.raises(ValueError, match="Транзакция не содержит поле 'currency'"):
            convert_to_rubles(transaction)

    def test_invalid_amount_type(self):
        """Некорректное значение amount"""
        transaction = {"amount": "invalid", "currency": "USD"}
        with pytest.raises(ValueError, match="Некорректное значение amount"):
            convert_to_rubles(transaction)

    def test_conversion_rate_none(self):
        """Курс не получен — должна быть ошибка"""
        transaction = {"amount": 100, "currency": "USD"}

        with patch('src.external_api.get_exchange_rate', return_value=None):
            with pytest.raises(ValueError, match="Не удалось получить курс для валюты USD"):
                convert_to_rubles(transaction)
