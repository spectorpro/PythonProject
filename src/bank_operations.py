import re
from typing import Any
from typing import Dict
from typing import List


def process_bank_search(data: List[Dict[str, Any]], search: str) -> List[Dict[str, Any]]:
    """
    Ищет транзакции по строке в описании с использованием регулярных выражений.

    Args:
        data: список словарей с данными о банковских операциях
        search: строка поиска

    Returns:
        Список словарей, у которых в описании есть данная строка
    """
    pattern = re.compile(re.escape(search), re.IGNORECASE)
    result = []
    for transaction in data:
        description = transaction.get('description', '')
        if pattern.search(description):
            result.append(transaction)
    return result


def process_bank_operations(data: List[Dict[str, Any]], categories: List[str]) -> Dict[str, int]:
    """
    Подсчитывает количество операций в каждой категории.

    Args:
        data: список словарей с данными о банковских операциях
        categories: список категорий операций

    Returns:
        Словарь с количеством операций в каждой категории
    """
    result = {category: 0 for category in categories}
    for transaction in data:
        description = transaction.get('description', '').lower()
        for category in categories:
            if category.lower() in description:
                result[category] += 1
    return result
