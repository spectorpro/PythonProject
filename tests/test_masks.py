import pytest
from src.masks import get_mask_card_number, get_mask_account


def test_standard_16_digit_card():
    """Тест с обычным 16‑значным номером карты."""
    result = get_mask_card_number("1234567890123456")
    assert result == "1234 56** **** 3456"

def test_card_with_spaces():
    """Тест с номером карты, содержащим пробелы."""
    result = get_mask_card_number("1234 5678 9012 3456")
    assert result == "1234 56** **** 3456"

@pytest.fixture
def card_with_dashes():
    return "1234 56** **** 3456"

def test_card_with_dashes(card_with_dashes):
    assert get_mask_card_number("1234567890123456") == card_with_dashes