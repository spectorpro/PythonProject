from typing import Any
from typing import Dict
from typing import Generator
from typing import Iterator


def filter_by_currency(transactions: list[Dict[str, Any]], currency_code: str) -> Iterator[Dict[str, Any]]:
    """
    Функция перебирает список транзакций и поочерёдно выдаёт те, где код валюты
    в поле operationAmount.currency.code соответствует заданному. Если какие‑либо
    промежуточные поля отсутствуют, транзакция пропускается без ошибок.
    """
    for transaction in transactions:
        # Проверяем, что в транзакции есть поле operationAmount
        if 'operationAmount' not in transaction:
            continue

        operation_amount = transaction['operationAmount']

        # Проверяем, что в operationAmount есть поле currency
        if 'currency' not in operation_amount:
            continue

        currency = operation_amount['currency']

        # Проверяем, что в currency есть поле code и оно соответствует искомому
        if 'code' in currency and currency['code'] == currency_code:
            yield transaction


def transaction_descriptions(transactions: list[dict]) -> Generator[str]:
    """Генератор transaction_descriptions,
    который принимает список словарей с транзакциями и возвращает
    описание каждой операции по очереди.
    """
    description_templates = [
        "Перевод организации",
        "Перевод со счета на счет",
        "Перевод с карты на карту"
    ]
    num_templates = len(description_templates)
    for i, transaction in enumerate(transactions):
        yield description_templates[i % num_templates]


def card_number_generator(start: int, end: int) -> Generator[str, None, None]:
    """Генератор card_number_generator,
    который выдает номера банковских карт в формате XXXX XXXX XXXX XXXX,
    где X— цифра номера карты.
    Генератор может сгенерировать номера карт в заданном диапазоне от 0000 0000 0000 0001
    до 9999 9999 9999 9999.
    """
    if not (1 <= start <= 9999999999999999):
        raise ValueError("Начальное значение должно быть в диапазоне от 1 до 9999999999999999")
    if not (1 <= end <= 9999999999999999):
        raise ValueError("Конечное значение должно быть в диапазоне от 1 до 9999999999999999")
    if start > end:
        raise ValueError("Начальное значение не может быть больше конечного")
    for number in range(start, end + 1):
        number_str = f"{number:016d}"
        formatted_card = ' '.join(number_str[i:i + 4] for i in range(0, 16, 4))
        yield formatted_card
