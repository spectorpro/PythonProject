import json
import os
from typing import List, Dict


def load_transactions(file_path: str) -> List[Dict]:
    """
    Загружает транзакции из локального JSON‑файла.

    Args:
        file_path (str): Путь к JSON‑файлу.

    Returns:
        List[Dict]: Список словарей с транзакциями или пустой список в случае ошибки.
    """
    # Проверяем существование файла
    if not os.path.exists(file_path):
        print(f"Ошибка: Файл не найден: {file_path}")
        return []

    # Пытаемся открыть и прочитать файл
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

            # Проверяем, что данные — это список
            if isinstance(data, list):
                return data
            else:
                print("Ошибка: JSON не содержит список транзакций")
                return []
    except json.JSONDecodeError:
        print("Ошибка: Некорректный JSON в файле")
        return []
    except IOError as e:
        print(f"Ошибка чтения файла: {e}")
        return []
