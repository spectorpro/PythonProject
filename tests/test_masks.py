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



@pytest.fixture
def invalid_card_numbers():
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
def edge_case_card_numbers():
    """Фикстура с пограничными случаями."""
    return [
        "1234567890",  # ровно 10 цифр
        "12345678901",  # 11 цифр
        "1" * 20,  # очень длинный номер
    ]

def test_invalid_card_numbers(invalid_card_numbers):
    """Тест невалидных номеров карт — должны вызывать ValueError."""
    for card in invalid_card_numbers:
        with pytest.raises(ValueError):
            get_mask_card_number(card)

def test_edge_cases(edge_case_card_numbers):
    """Тест пограничных случаев."""
    # Ровно 10 цифр: первые 6 и последние 4, между ними нет звёздочек
    result_10 = get_mask_card_number("1234567890")
    assert result_10 == "1234 5678 90"

    # 11 цифр: первые 6, одна звёздочка, последние 4
    result_11 = get_mask_card_number("12345678901")
    assert result_11 == "1234 56*8 901"

    # Очень длинный номер: проверяем сохранение длины
    long_card = "1" * 20
    result_long = get_mask_card_number(long_card)
    assert len(result_long.replace(" ", "")) == 20
