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
