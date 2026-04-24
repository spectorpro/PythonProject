import pytest
from src.widget import mask_account_card, get_date

@pytest.fixture
def card_test_cases():
    """Фикстура с тестовыми случаями для карт."""
    return [
        ("Visa Classic 6831982476737658", "Visa Classic 6831 98** **** 7658"),
        ("MasterCard 5555123456789012", "MasterCard 5555 12** **** 9012"),
        ("American Express 378282246310005", "American Express 3782 82** ***0 005"),
        ("Discover 6011111111111117", "Discover 6011 11** **** 1117"),
        ("Maestro 6759000000000001", "Maestro 6759 00** **** 0001"),
    ]

@pytest.fixture
def account_test_cases():
    """Фикстура с тестовыми случаями для счетов."""
    return [
        ("Счет 75106830613657916952", "Счет **6952"),
        ("Счёт 19708645243227258542", "Счёт **8542"),
        ("Накопительный счет 44812258784861134719", "Накопительный счет 4481 22** **** **** 4719"),
        ("Сберегательный счёт 12345678901234567890", "Сберегательный счёт 1234 56** **** **** 7890"),
    ]

@pytest.fixture
def mixed_test_cases():
    """Фикстура со смешанными тестовыми случаями."""
    return [
        ("Visa 4111111111111111", "Visa 4111 11** **** 1111"),
        ("Счет 11112222333344445555", "Счет **5555"),
        ("Debit Card 5212345678901234", "Debit Card 5212 34** **** 1234"),
        ("Текущий счёт 99998888777766665555", "Текущий счёт 9999 88** **** **** 5555"),
    ]

@pytest.fixture
def edge_cases():
    """Фикстура с граничными случаями и ошибками."""
    return [
        ("", None),  # Пустая строка
        ("Без цифр и номера", None),  # Нет цифр
        ("Карта ", None),  # Только префикс, нет номера
        ("Счет ABC123DEF", None),  # Буквы и цифры смешанно, но нет чистого номера
    ]






def test_cards_from_fixture(card_test_cases):
    """Тесты для карт с использованием фикстуры."""
    for input_str, expected in card_test_cases:
        result = mask_account_card(input_str)
        assert result == expected, f"Failed for: {input_str}"

def test_accounts_from_fixture(account_test_cases):
    """Тесты для счетов с использованием фикстуры."""
    for input_str, expected in account_test_cases:
        result = mask_account_card(input_str)
        assert result == expected, f"Failed for: {input_str}"

def test_mixed_cases_from_fixture(mixed_test_cases):
    """Тесты со смешанными случаями из фикстуры."""
    for input_str, expected in mixed_test_cases:
        result = mask_account_card(input_str)
        assert result == expected, f"Failed for: {input_str}"

def test_edge_cases_from_fixture(edge_cases):
    """Тесты граничных случаев и ошибок из фикстуры."""
    for input_str, _ in edge_cases:
        if input_str == "":  # Пустая строка
            with pytest.raises(ValueError, match="Номер карты должен содержать не менее 10 цифр"):
                mask_account_card(input_str)
        elif "Без цифр" in input_str:  # Нет цифр в строке
            with pytest.raises(ValueError, match="Номер карты должен содержать не менее 10 цифр"):
                mask_account_card(input_str)
        elif input_str.endswith(" "):  # Только префикс
            with pytest.raises(ValueError, match="Номер карты должен содержать не менее 10 цифр"):
                mask_account_card(input_str)

@pytest.fixture
def test_data():
    return [
        {'id': 1, 'state': 'EXECUTED', 'date': '2024-03-11T02:26:18.671407'},
        {'id': 2, 'state': 'PENDING', 'date': '2023-12-25T15:30:45.123456'},
        {'id': 3, 'state': 'CANCELED', 'date': '2022-01-01T00:00:00.000000'},
        {'id': 4, 'state': 'FAILED', 'date': '2021-06-15T12:34:56.789012'},
        {'id': 5, 'state': 'COMPLETED', 'date': '2020-02-29T23:59:59.999999'},  # Високосный год
        {'id': 6, 'state': 'EXECUTED', 'date': '2019-04-04T23:20:05.206878'},
    ]

# Фикстура для граничных случаев дат
@pytest.fixture
def edge_case_dates():
    return [
        '2000-01-01T00:00:00.000000',  # Начало века
        '2100-12-31T23:59:59.999999',  # Конец века
        '1900-02-28T12:00:00.000000',  # Невисокосный год (1900)
        '2000-02-29T12:00:00.000000',  # Високосный год (2000)
    ]


# Тест: корректное преобразование дат из тестовых данных
def test_get_date_with_test_data(test_data):
    expected_results = {
        '2024-03-11T02:26:18.671407': '11.03.2024',
        '2023-12-25T15:30:45.123456': '25.12.2023',
        '2022-01-01T00:00:00.000000': '01.01.2022',
        '2021-06-15T12:34:56.789012': '15.06.2021',
        '2020-02-29T23:59:59.999999': '29.02.2020',
        '2019-04-04T23:20:05.206878': '04.04.2019',
    }

    for item in test_data:
        input_date = item['date']
        expected = expected_results[input_date]
        result = get_date(input_date)
        assert result == expected, f"Ошибка преобразования даты {input_date}: получено {result}, ожидалось {expected}"

# Тест: граничные случаи дат
def test_get_date_edge_cases(edge_case_dates):
    expected_results = [
        '01.01.2000',
        '31.12.2100',
        '28.02.1900',
        '29.02.2000',
    ]
