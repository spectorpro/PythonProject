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
    assert get_mask_card_number("1234-567890-123456") == card_with_dashes



def test_standard_20_digit_bank_account():
    """Тест с обычным 20‑значным номером счета."""
    result = get_mask_account("73654108430135874305")
    assert result == "**4305"



def test_card_with_spaces_bank_account():
    """Тест с номером счета, содержащим нециофровые символы."""
    result = get_mask_account("73f65410843f0135874305")
    assert result == "**4305"



def test_expected_length_bank_account():
    """Тест с номером счета, содержащим меньшую длину."""
    result = get_mask_account("7108430135874305")
    assert result == "**4305"


