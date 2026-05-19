import logging
import os
from typing import Dict
from typing import Optional

import requests
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

# Заданный API-ключ
API_KEY = "MYzzlLze2rEY9Er22o6K7GRLbbB1qj0Y"
BASE_URL = "https://api.apilayer.com/exchangerates_data/latest"


def get_exchange_rate(base_currency: str, target_currency: str = "RUB") -> Optional[float]:
    """
    Получает курс обмена валюты через API Apilayer с корректной обработкой ошибок.

    Args:
        base_currency (str): Исходная валюта.
        target_currency (str): Целевая валюта (по умолчанию RUB).

    Returns:
        Optional[float]: Курс обмена или None в случае ошибки.
    """
    if not API_KEY:
        logger.error("API ключ не найден")
        return None

    headers = {
        "apikey": API_KEY
    }
    params = {
        "base": base_currency,
        "symbols": target_currency
    }

    try:
        response = requests.get(
            BASE_URL,
            headers=headers,
            params=params,
            timeout=10  # Таймаут 10 секунд
        )

        # Обработка HTTP-ошибок
        if response.status_code == 401:
            logger.error("Ошибка аутентификации: неверный API ключ")
            return None
        elif response.status_code == 429:
            logger.error("Превышен лимит запросов к API")
            return None
        elif response.status_code != 200:
            logger.error(f"HTTP ошибка {response.status_code}: {response.text}")
            return None

        data = response.json()

        # Проверка структуры ответа API
        if not data.get("success", False):
            error_msg = data.get("error", {}).get("info", "Неизвестная ошибка API")
            logger.error(f"API вернуло ошибку: {error_msg}")
            return None

        if "rates" in data and target_currency in data["rates"]:
            rate = float(data["rates"][target_currency])
            logger.info(f"Получен курс: 1 {base_currency} = {rate} {target_currency}")
            return rate
        else:
            logger.error(f"Курс для {target_currency} не найден в ответе API")
            return None
    except requests.exceptions.Timeout:
        logger.error("Таймаут запроса к API (превышено 10 с)")
        return None
    except requests.exceptions.ConnectionError:
        logger.error("Ошибка подключения к API")
        return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Общая ошибка запроса к API: {e}")
        return None
    except (KeyError, ValueError, TypeError) as e:
        logger.error(f"Ошибка обработки ответа API: {e}")
        return None


def convert_to_rubles(transaction: Dict) -> float:
    """
    Конвертирует сумму транзакции в рубли с валидацией данных.

    Args:
        transaction (Dict): Транзакция с полями 'amount' и 'currency'.

    Returns:
        float: Сумма в рублях.

    Raises:
        ValueError: Если транзакция содержит некорректные данные.
    """
    # Валидация входных данных
    if not isinstance(transaction, dict):
        raise ValueError("Транзакция должна быть словарем")

    amount = transaction.get("amount")
    currency = transaction.get("currency")

    if amount is None:
        raise ValueError("Транзакция не содержит поле 'amount'")
    if currency is None:
        raise ValueError("Транзакция не содержит поле 'currency'")

    try:
        amount = float(amount)
    except (ValueError, TypeError):
        raise ValueError(f"Некорректное значение amount: {amount}")

    if currency == "RUB":
        logger.info(f"Транзакция в RUB: {amount} RUB")
        return amount

    rate = get_exchange_rate(currency)
    if rate is not None:
        result = amount * rate
        logger.info(f"Конвертация: {amount} {currency} = {result:.2f} RUB (курс: {rate})")
        return result
    else:
        raise ValueError(f"Не удалось получить курс для валюты {currency}")
