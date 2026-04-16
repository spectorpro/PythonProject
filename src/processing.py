from datetime import datetime

def filter_by_state(data_list, state='EXECUTED'):
    """
    Фильтрует список словарей по значению ключа 'state'.

    Args:
        data_list (list): Список словарей с данными.
        state (str): Значение ключа 'state' для фильтрации (по умолчанию 'EXECUTED').

    Returns:
        list: Новый список словарей, где значение ключа 'state' соответствует указанному.
    """
    return [item for item in data_list if item.get('state') == state]



def sort_by_date(data_list, reverse=True):
    """
    Сортирует список словарей по дате (ключ 'date').

    Args:
        data_list (list): Список словарей с данными, содержащими ключ 'date'.
        reverse (bool): Порядок сортировки: True — убывание (по умолчанию), False — возрастание.

    Returns:
        list: Новый отсортированный список словарей.
    """
    def parse_date(date_string):
        # Преобразуем строку даты в объект datetime для корректной сортировки
        return datetime.fromisoformat(date_string.replace('Z', '+00:00'))

    return sorted(
        data_list,
        key=lambda x: parse_date(x['date']),
        reverse=reverse
    )