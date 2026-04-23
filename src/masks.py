def get_mask_card_number(card_number: str) -> str:
    """
    Маскирует номер банковской карты.

    Принимает на вход номер карты и возвращает его маску в формате:
    XXXX XX** **** XXXX (видны первые 6 и последние 4 цифры, остальные — звёздочки).
    Номер разбит по блокам по 4 цифры, разделённым пробелами.

    Args:
        card_number (str): Номер карты (строка из цифр).

    Returns:
        str: Замаскированный номер карты.
    """
    # Убираем все нецифровые символы (пробелы, дефисы и т.д.)
    digits = "".join(filter(str.isdigit, card_number))

    # Проверяем, что номер содержит достаточно цифр (минимум 10)
    if len(digits) < 10:
        raise ValueError("Номер карты должен содержать не менее 10 цифр")

    # Берём первые 6 цифр и последние 4 цифры
    first_part = digits[:6]
    last_part = digits[-4:]

    # Создаём маску: между первой и последней частью — звёздочки
    # Всего цифр в маске (без пробелов) — столько же, сколько в оригинале
    masked_middle = "*" * (len(digits) - 10)  # 10 = 6 + 4
    full_masked = first_part + masked_middle + last_part

    # Разбиваем на блоки по 4 символа, разделяем пробелами
    blocks = [full_masked[i : i + 4] for i in range(0, len(full_masked), 4)]
    result = " ".join(blocks)

    return result


def get_mask_account(account_number: str) -> str:
    """
    Маскирует номер банковского счёта.

    Принимает на вход номер счёта и возвращает его маску в формате **XXXX,
    где видны только последние 4 цифры, а перед ними — две звёздочки.

    Args:
        account_number (str): Номер счёта (строка из цифр).

    Returns:
        str: Замаскированный номер счёта.
    """
    # Убираем все нецифровые символы
    digits = "".join(filter(str.isdigit, account_number))

    # Проверяем, что номер содержит достаточно цифр (минимум 4)
    if len(digits) < 4:
        raise ValueError("Номер счёта должен содержать не менее 4 цифр")

    # Берём последние 4 цифры
    last_four = digits[-4:]

    # Формируем маску: две звёздочки и последние 4 цифры
    result = f"**{last_four}"

    return result


# Примеры использования
#if __name__ == "__main__":
     #Пример для карты
    #card = "7000792289606361"
    #print(f"{card}  # входной аргумент")
    #print(f"{get_mask_card_number(card)}  # выход функции")

    # Пример для счёта
    #account = "73654108430135874305"
    #print(f"\n{account}  # входной аргумент")
    #print(f"{get_mask_account(account)}  # выход функции")
