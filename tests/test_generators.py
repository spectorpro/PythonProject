from typing import Any
from typing import Dict
from typing import Generator
from typing import List

import pytest

from src.generators import card_number_generator
from src.generators import filter_by_currency
from src.generators import transaction_descriptions


@pytest.fixture
def sample_transactions() -> List[Dict[str, Any]]:
    """Фикстура: тестовые транзакции с разными валютами."""
    return [
        {
            'id': 1,
            'operationAmount': {
                'amount': 100,
                'currency': {'code': 'USD', 'name': 'US Dollar'}
            }
        },
        {
            'id': 2,
            'operationAmount': {
                'amount': 200,
                'currency': {'code': 'EUR', 'name': 'Euro'}
            }
        },
        {
            'id': 3,
            'operationAmount': {
                'amount': 300,
                'currency': {'code': 'USD', 'name': 'US Dollar'}
            }
        },
        {
            'id': 4,
            'operationAmount': {
                'amount': 400,
                'currency': {'code': 'GBP', 'name': 'British Pound'}
            }
        }
    ]


# Фикстура для транзакций с неполными данными
@pytest.fixture
def incomplete_transactions() -> List[Dict[str, Any]]:
    """Фикстура: транзакции с отсутствующими полями."""
    return [
        {'id': 5, 'amount': 500},  # Нет operationAmount
        {
            'id': 6,
            'operationAmount': {'amount': 600}  # Нет currency
        },
        {
            'id': 7,
            'operationAmount': {
                'amount': 700,
                'currency': {'name': 'Unknown Currency'}  # Нет code
            }
        },
        {},  # Полностью пустая транзакция
        {'operationAmount': {}},  # operationAmount без currency
        {'operationAmount': {'currency': {}}}  # currency без code
    ]


# Фикстура для пустой транзакции
@pytest.fixture
def empty_transactions() -> List[Dict[str, Any]]:
    """Фикстура: пустой список транзакций."""
    return []


def test_filter_usd_transactions(sample_transactions: List[Dict[str, Any]]) -> None:
    """Тест фильтрации транзакций в USD."""
    result: List[Dict[str, Any]] = list(filter_by_currency(sample_transactions, 'USD'))
    assert len(result) == 2
    assert result[0]['id'] == 1
    assert result[1]['id'] == 3


def test_filter_eur_transactions(sample_transactions: List[Dict[str, Any]]) -> None:
    """Тест фильтрации транзакций в EUR."""
    result: List[Dict[str, Any]] = list(filter_by_currency(sample_transactions, 'EUR'))
    assert len(result) == 1
    assert result[0]['id'] == 2


def test_no_transactions_in_currency(sample_transactions: List[Dict[str, Any]]) -> None:
    """Тест случая, когда транзакции в заданной валюте отсутствуют."""
    result: List[Dict[str, Any]] = list(filter_by_currency(sample_transactions, 'JPY'))
    assert len(result) == 0


def test_empty_transactions_list(empty_transactions: List[Dict[str, Any]]) -> None:
    """Тест обработки пустого списка транзакций."""
    result: List[Dict[str, Any]] = list(filter_by_currency(empty_transactions, 'USD'))
    assert len(result) == 0


def test_currency_without_code(sample_transactions: List[Dict[str, Any]], incomplete_transactions: List[Dict[str, Any]]) -> None:
    """Тест пропуска транзакций, где в currency нет поля code."""
    transactions_with_missing_code: List[Dict[str, Any]] = (
            sample_transactions + [incomplete_transactions[2]]
    )
    result: List[Dict[str, Any]] = list(
        filter_by_currency(transactions_with_missing_code, 'USD')
    )
    assert len(result) == 2


@pytest.fixture
def sample_transactions_one() -> List[Dict]:
    """Фикстура: набор тестовых транзакций для проверки."""
    return [
        {"amount": 1000, "type": "transfer"},
        {"amount": 500, "type": "internal"},
        {"amount": 200, "type": "card"},
        {"amount": 300, "type": "another"}
    ]


def test_multiple_transactions_exact_match(sample_transactions_one: List[Dict]) -> None:
    """Тест: проверка работы с количеством транзакций, равным числу шаблонов."""
    # Берём первые 3 транзакции — их количество равно числу шаблонов
    subset = sample_transactions_one[:3]
    result = list(transaction_descriptions(subset))
    expected = [
        "Перевод организации",
        "Перевод со счета на счет",
        "Перевод с карты на карту"
    ]
    assert result == expected, "Шаблоны должны применяться последовательно без повторов"


@pytest.fixture
def empty_transactions_one() -> List[Dict]:
    """Фикстура: пустой список транзакций."""
    return []


def test_empty_transactions(empty_transactions_one: List[Dict]) -> None:
    """Тест: проверка работы с пустым списком транзакций."""
    result = list(transaction_descriptions(empty_transactions_one))
    assert result == [], "Для пустого списка должен возвращаться пустой генератор"


@pytest.fixture
def single_transaction() -> List[Dict]:
    """Фикстура: одна транзакция."""
    return [{"amount": 1500, "type": "single"}]


def test_single_transaction(single_transaction: List[Dict]) -> None:
    """Тест: проверка работы с одной транзакцией."""
    result = list(transaction_descriptions(single_transaction))
    expected = ["Перевод организации"]
    assert result == expected, "Для одной транзакции должен применяться первый шаблон"


@pytest.mark.parametrize("start,end,expected_first,expected_last", [
        (1, 1, "0000 0000 0000 0001", "0000 0000 0000 0001"),
        (9999999999999998, 9999999999999999, "9999 9999 9999 9998", "9999 9999 9999 9999"),
        (1234567890123456, 1234567890123457, "1234 5678 9012 3456", "1234 5678 9012 3457"),
    ])
def test_correct_range_and_formatting(start: int, end: int, expected_first: str, expected_last: str) -> None:
    """
    Тест проверяет:
    - корректность диапазона генерируемых номеров;
    - правильность форматирования (формат XXXX XXXX XXXX XXXX);
    - обработку крайних значений диапазона.
    """
    generator: Generator[str, None, None] = card_number_generator(start, end)
    results: list[str] = list(generator)

    assert len(results) == end - start + 1
    assert results[0] == expected_first
    assert results[-1] == expected_last

    for card_number in results:
        assert len(card_number) == 19  # 16 цифр + 3 пробела
        assert card_number.count(' ') == 3
        parts = card_number.split(' ')
        assert all(len(part) == 4 for part in parts)
        assert all(part.isdigit() for part in parts)


@pytest.mark.parametrize("start,end", [
        (1, 5),
        (9999999999999995, 9999999999999999),
        (1000000000000000, 1000000000000005),
    ])
def test_consistent_generation(start: int, end: int) -> None:
    """Тест проверяет, что генератор последовательно выдаёт все номера в диапазоне."""
    generator: Generator[str, None, None] = card_number_generator(start, end)
    results: list[str] = list(generator)
    expected_count: int = end - start + 1

    assert len(results) == expected_count

    for i, card_number in enumerate(results):
        expected_number: int = start + i
        expected_formatted: str = ' '.join(f"{expected_number:016d}"[j:j + 4] for j in range(0, 16, 4))
        assert card_number == expected_formatted
