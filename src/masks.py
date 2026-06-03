import logging
import os

# Создаём отдельный объект логера для модуля masks
logger = logging.getLogger('masks')
logger.setLevel(logging.DEBUG)  # Уровень логирования не меньше, чем DEBUG


log_dir = r'PythonProject1\logs'
os.makedirs(log_dir, exist_ok=True)
# Настраиваем обработчик для записи в файл
file_handler = logging.FileHandler(os.path.join(log_dir, 'masks.log'), mode='a', encoding='utf-8')
file_handler.setLevel(logging.DEBUG)

# Настраиваем форматтер для логера модуля masks
file_formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Устанавливаем форматтер для обработчика
file_handler.setFormatter(file_formatter)

# Добавляем обработчик к логеру модуля masks
logger.addHandler(file_handler)


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

    logger.debug(f"Начало обработки номера карты: '{card_number}'")
    # Убираем все нецифровые символы (пробелы, дефисы и т.д.)
    digits = "".join(filter(str.isdigit, card_number))
    logger.debug(f"Извлечены цифры: '{digits}' (длина: {len(digits)})")

    # Проверяем, что номер содержит достаточно цифр (минимум 10)
    if len(digits) < 10:
        error_msg = f"Номер карты должен содержать не менее 10 цифр. Получено: {len(digits)}"
        logger.error(error_msg)  # Логирование ошибочных случаев с уровнем не ниже ERROR
        raise ValueError(error_msg)

    logger.info(f"Номер карты валиден, длина: {len(digits)} цифр")

    # Берём первые 6 цифр и последние 4 цифры
    first_part = digits[:6]
    last_part = digits[-4:]
    logger.debug(f"Первые 6 цифр: '{first_part}', последние 4 цифры: '{last_part}'")

    # Создаём маску: между первой и последней частью — звёздочки
    # Всего цифр в маске (без пробелов) — столько же, сколько в оригинале
    masked_middle = "*" * (len(digits) - 10)  # 10 = 6 + 4
    full_masked = first_part + masked_middle + last_part
    logger.debug(f"Создана полная маска (без форматирования): '{full_masked}'")

    # Разбиваем на блоки по 4 символа, разделяем пробелами
    blocks = [full_masked[i:i + 4] for i in range(0, len(full_masked), 4)]
    result = " ".join(blocks)
    logger.info(f"Замаскированный номер создан: '{result}'")  # Логирование успешного случая

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
    logger.debug(f"Извлечены цифры: '{digits}' (длина: {len(digits)})")

    # Проверяем, что номер содержит достаточно цифр (минимум 4)
    if len(digits) < 4:
        error_msg = f"Номер счёта должен содержать не менее 4 цифр. Получено: {len(digits)}"
        logger.error(error_msg)  # Логирование ошибочных случаев с уровнем не ниже ERROR
        raise ValueError(error_msg)

    logger.info(f"Номер счёта валиден, длина: {len(digits)} цифр")

    # Берём последние 4 цифры
    last_four = digits[-4:]
    logger.debug(f"Последние 4 цифры: '{last_four}'")

    # Формируем маску: две звёздочки и последние 4 цифры
    result = f"**{last_four}"
    logger.info(f"Замаскированный номер счёта создан: '{result}'")  # Логирование успешного случая

    return result
