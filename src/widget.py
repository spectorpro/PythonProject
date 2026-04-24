from src.masks import get_mask_account, get_mask_card_number
"""
Переиспользование уже существующих функций
"""


def mask_account_card(account_or_card: str) -> str:
    """
    Обрабатывает информацию о картах и счетах, возвращая строку с замаскированным номером.

    Для карт и счетов используются разные типы маскировки.
    Переиспользуются существующие функции маскировки.

    Args:
        account_or_card (str): Строка, содержащая тип и номер карты или счёта.

    Returns:
        str: Строка с замаскированным номером.
    """
    # Определяем, является ли запись счётом (ищем слово «Счёт» или «Счет»)
    is_account = 'Счет' in account_or_card or 'Счёт' in account_or_card

    # Извлекаем номер — все цифры из строки
    digits = ''.join(filter(str.isdigit, account_or_card))

    if is_account:
        # Для счёта используем соответствующую функцию маскировки
        masked_number = get_mask_account(digits)
    else:
        # Для карты используем функцию маскировки карты
        masked_number = get_mask_card_number(digits)

    # Получаем часть строки до номера (название карты/счёта)
    # Ищем последнее вхождение цифры — это начало номера
    number_start = None
    for i, char in enumerate(account_or_card):
        if char.isdigit():
            number_start = i
            break

    if number_start is None:
        raise ValueError("В строке не найден номер")

    prefix = account_or_card[:number_start].strip()

    # Формируем итоговую строку
    result = f"{prefix} {masked_number}"
    return result


def get_date(str_date: str) -> str:
    """
    Преобразует строку с датой из формата "2024-03-11T02:26:18.671407"
    в формат "ДД.ММ.ГГГГ" ("11.03.2024").

    Args:
        str_date (str): Исходная строка с датой.

    Returns:
        str: Дата в формате "ДД.ММ.ГГГГ".
    """
    # Разделяем дату и время по символу 'T'
    date_part = str_date.split('T')[0]
    # Разделяем год, месяц и день
    year, month, day = date_part.split('-')
    # Форматируем в нужный вид
    formatted_date = f"{day}.{month}.{year}"
    return formatted_date
