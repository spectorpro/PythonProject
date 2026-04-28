from typing import Iterator, Dict, Any

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

