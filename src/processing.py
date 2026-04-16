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


# Тестовые данные
test_data = [
    {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
    {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
    {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
    {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
]

# Проверка filter_by_state
print("Фильтрация по 'EXECUTED':")
print(filter_by_state(test_data))
print("\nФильтрация по 'CANCELED':")
print(filter_by_state(test_data, 'CANCELED'))

# Проверка sort_by_date
print("\nСортировка по убыванию (по умолчанию):")
print(sort_by_date(test_data))
print("\nСортировка по возрастанию:")
print(sort_by_date(test_data, reverse=False))
