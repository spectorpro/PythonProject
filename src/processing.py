from datetime import datetime
from typing import List, Dict, Any


def filter_by_state(
    data_list: List[Dict[str, Any]],
    state: str = 'EXECUTED'
) -> List[Dict[str, Any]]:
    """
    Фильтрует список словарей по значению ключа 'state'.

    Args:
        data_list (List[Dict[str, Any]]): Список словарей с данными.
        state (str): Значение ключа 'state' для фильтрации (по умолчанию 'EXECUTED').

    Returns:
        List[Dict[str, Any]]: Новый список словарей, где значение ключа 'state' соответствует указанному.
    """
    return [item for item in data_list if item.get('state') == state]


def sort_by_date(
    data_list: List[Dict[str, Any]],
    reverse: bool = True
) -> List[Dict[str, Any]]:
    """
    Сортирует список словарей по дате (ключ 'date').

    Args:
        data_list (List[Dict[str, Any]]): Список словарей с данными, содержащими ключ 'date'.
        reverse (bool): Порядок сортировки: True — убывание (по умолчанию), False — возрастание.

    Returns:
        List[Dict[str, Any]]: Новый отсортированный список словарей.
    """
    def parse_date(date_string: str) -> datetime:
        # Преобразуем строку даты в объект datetime для корректной сортировки
        return datetime.fromisoformat(date_string.replace('Z', '+00:00'))

    return sorted(
        data_list,
        key=lambda x: parse_date(x['date']),
        reverse=reverse
    )
