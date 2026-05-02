from typing import List

import pytest

from src.masks import get_mask_account
from src.masks import get_mask_card_number


def test_standard_16_digit_card() -> None:
    """Тест с обычным 16‑значным номером карты."""
    result: str = get_mask_card_number("1234567890123456")
    assert result == "1234 56** **** 3456"


def test_card_with_spaces() -> None:
    """Тест с номером карты, содержащим пробелы."""
    result: str = get_mask_card_number("1234 5678 9012 3456")
    assert result == "1234 56** **** 3456"


@pytest.fixture
def card_with_dashes() -> str:
    return "1234 56** **** 3456"


def test_card_with_dashes(card_with_dashes: str) -> None:
    assert get_mask_card_number("1234-567890-123456") == card_with_dashes


def test_standard_20_digit_bank_account() -> None:
    """Тест с обычным 20‑значным номером счёта."""
    result: str = get_mask_account("73654108430135874305")
    assert result == "**4305"


def test_card_with_spaces_bank_account() -> None:
    """Тест с номером счёта, содержащим нечисловые символы."""
    result: str = get_mask_account("73f65410843f0135874305")
    assert result == "**4305"


def test_expected_length_bank_account() -> None:
    """Тест с номером счёта, содержащим меньшую длину."""
    result: str = get_mask_account("7108430135874305")
    assert result == "**4305"


@pytest.fixture
def invalid_card_numbers() -> List[str]:
    """Фикстура с невалидными номерами карт."""
    return [
        "1234",  # слишком короткий
        "12345",  # недостаточно цифр
        "",  # пустая строка
        "abc123",  # только буквы
        "----",  # только дефисы
        "   ",  # только пробелы
    ]


@pytest.fixture
def edge_case_card_numbers() -> List[str]:
    """Фикстура с пограничными случаями."""
    return [
        "1234567890",  # ровно 10 цифр
        "12345678901",  # 11 цифр
        "1" * 20,  # очень длинный номер
    ]


def test_invalid_card_numbers(invalid_card_numbers: List[str]) -> None:
    """Тест невалидных номеров карт — должны вызывать ValueError."""
    for card in invalid_card_numbers:
        with pytest.raises(ValueError):
            get_mask_card_number(card)


def test_edge_cases(edge_case_card_numbers: List[str]) -> None:
    """Тест пограничных случаев."""
    # Ровно 10 цифр: первые 6 и последние 4, между ними нет звёздочек
    result_10: str = get_mask_card_number("1234567890")
    assert result_10 == "1234 5678 90"

    # 11 цифр: первые 6, одна звёздочка, последние 4
    result_11: str = get_mask_card_number("12345678901")
    assert result_11 == "1234 56*8 901"

    # Очень длинный номер: проверяем сохранение длины
    long_card: str = "1" * 20
    result_long: str = get_mask_card_number(long_card)
    assert len(result_long.replace(" ", "")) == 20


@pytest.fixture
def invalid_account_numbers() -> List[str]:
    """Фикстура с невалидными номерами счетов."""
    return [
        "123",  # слишком короткий
        "12",  # недостаточно цифр
        "",  # пустая строка
        "abc123",  # только буквы
        "----",  # только дефисы
        "   ",  # только пробелы
        "1a2b3c",  # смешанные символы без цифр
    ]


@pytest.fixture
def edge_case_account_numbers() -> List[str]:
    """Фикстура с пограничными случаями."""
    return [
        "1234",  # ровно 4 цифры
        "12345",  # 5 цифр
        "1" * 30,  # очень длинный номер (30 цифр)
    ]


def test_invalid_account_numbers(invalid_account_numbers: List[str]) -> None:
    """Тест невалидных номеров счетов — должны вызывать ValueError."""
    for account in invalid_account_numbers:
        with pytest.raises(ValueError, match="Номер счёта должен содержать не менее 4 цифр"):
            get_mask_account(account)


def test_edge_cases_two(edge_case_account_numbers: List[str]) -> None:
    """Тест пограничных случаев."""
    # Ровно 4 цифры: должны видеть все 4 цифры после **
    result_4: str = get_mask_account("1234")
    assert result_4 == "**1234"

    # 5 цифр: должны видеть последние 4 после **
    result_5: str = get_mask_account("12345")
    assert result_5 == "**2345"

    # Очень длинный номер: проверяем, что видим только последние 4 цифры
    long_account: str = "1" * 30
    result_long: str = get_mask_account(long_account)
    assert result_long == "**1111"
