import json
import os
from typing import List, Dict
import logging

# Настройка логирования вместо print
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_transactions(file_path: str) -> List[Dict]:
    """
    Загружает транзакции из локального JSON‑файла с детальной обработкой ошибок.

    Args:
        file_path (str): Путь к JSON‑файлу.

    Returns:
        List[Dict]: Список словарей с транзакциями или пустой список в случае ошибки.
    """
    # Проверка существования файла
    if not os.path.exists(file_path):
        logger.error(f"Файл не найден: {file_path}")
        return []

    # Проверка, что это файл (а не директория)
    if not os.path.isfile(file_path):
        logger.error(f"Указанный путь не является файлом: {file_path}")
        return []

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            try:
                data = json.load(file)

                # Проверка, что данные — это список
                if isinstance(data, list):
                    logger.info(f"Успешно загружено {len(data)} транзакций")
                    return data
                else:
                    logger.error("JSON не содержит список транзакций")
                    return []
            except json.JSONDecodeError as e:
                logger.error(f"Ошибка парсинга JSON: {e}")
                return []
    except PermissionError:
        logger.error(f"Нет прав доступа к файлу: {file_path}")
        return []
    except IsADirectoryError:
        logger.error(f"Указан путь к директории вместо файла: {file_path}")
        return []
    except UnicodeDecodeError as e:
        logger.error(f"Ошибка кодировки файла: {e}")
        return []
    except OSError as e:
        logger.error(f"OS ошибка при чтении файла: {e}")
        return []
