import os
import requests
from dotenv import load_dotenv
from typing import Optional

load_dotenv()

API_KEY = os.getenv('EXCHANGE_API_KEY')
BASE_URL = 'https://api.apilayer.com/exchangerates_data/latest'


def get_exchange_rate(base_currency: str, target_currency: str = 'RUB') -> Optional[float]:
    """
    Получает курс обмена валюты через API Apilayer.

    Args:
        base_currency (str): Исходная валюта.
        target_currency (str): Целевая валюта (по умолчанию RUB).

    Returns:
        Optional[float]: Курс обмена или None в случае ошибки.
    """
    headers = {
        'apikey': API_KEY
    }
    params = {
        'base': base_currency,
        'symbols': target_currency
    }

    try:
        response = requests.get(BASE_URL, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

        if 'rates' in data and target_currency in data['rates']:
            return float(data['rates'][target_currency])
        else:
            print(f"Ошибка: Курс для {target_currency} не найден в ответе API")
            return None
    except requests.RequestException as e:
        print(f"Ошибка запроса к API: {e}")
        return None
    except (KeyError, ValueError) as e:
        print(f"Ошибка обработки ответа API: {e}")
        return None


def convert_to_rubles(transaction: Dict) -> float:
    """
    Конвертирует сумму транзакции в рубли.

    Args:
        transaction (Dict): Транзакция с полями 'amount' и 'currency'.

    Returns:
        float: Сумма в рублях.
    """
    amount = transaction.get('amount', 0.0)
    currency = transaction.get('currency', 'RUB')

    if currency == 'RUB':
        return float(amount)

    rate = get_exchange_rate(currency)
    if rate is not None:
        return float(amount * rate)
    else:
        raise ValueError(f"Не удалось получить курс для валюты {currency}")
