import datetime
from typing import Any
from typing import Dict
from typing import List

from src.bank_operations import process_bank_search
from src.data_loaders import load_csv_data
from src.data_loaders import load_json_data
from src.data_loaders import load_xlsx_data
from src.widget import mask_account_card, get_date


def filter_by_status(data: List[Dict[str, Any]], status: str) -> List[Dict[str, Any]]:
    """Фильтрует транзакции по статусу (с приведением к единому регистру)."""
    status_upper = status.upper()
    valid_statuses = {'EXECUTED', 'CANCELED', 'PENDING'}
    if status_upper not in valid_statuses:
        raise ValueError(f"Статус операции '{status}' недоступен.")
    return [t for t in data if t.get('state', '') == status_upper]


def sort_by_date(data: List[Dict[str, Any]], ascending: bool = True) -> List[Dict[str, Any]]:
    """Сортирует транзакции по дате."""
    def parse_date(date_str: str) -> datetime.datetime:
        try:
            return datetime.datetime.strptime(date_str, '%d.%m.%Y')
        except ValueError:
            return datetime.datetime.min
    return sorted(data, key=lambda x: parse_date(x.get('date', '')), reverse=not ascending)


def filter_ruble_transactions(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Оставляет только рублёвые транзакции."""
    return [t for t in data if "RUB" in str(t.get('currency_code', ''))]


def filter_ruble_transactions_json(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Оставляет только рублёвые транзакции."""
    return [
        t for t in data
        if t.get('operationAmount', {}).get('currency', {}).get('code') == 'RUB'
    ]


def print_transactions(transactions: List[Dict[str, Any]]):
    """Выводит транзакции в консоль в заданном формате с маскировкой счетов/карт и форматированием даты."""
    if not transactions:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return
    print(f"Всего банковских операций в выборке: {len(transactions)}")
    for t in transactions:
        date = get_date(t.get('date', ''))
        desc = t.get('description', '')
        amount = t.get('amount', '')
        valuta = t.get('currency_code', '')

        from_field = t.get('from', '')
        masked_from = mask_account_card(from_field) if from_field else ''

        to_field = t.get('to', '')
        masked_to = mask_account_card(to_field) if to_field else ''

        if masked_from and masked_to:
            print(f"{date} {desc}\n{masked_from} -> {masked_to}\nСумма: {amount} {valuta}")
        elif masked_from:
            print(f"{date} {desc}\n{masked_from}\nСумма: {amount} {valuta}")
        elif masked_to:
            print(f"{date} {desc}\n{masked_to}\nСумма: {amount} {valuta}")
        else:
            print(f"{date} {desc}\nСумма: {amount} {valuta}")


def print_transactions_json(transactions: List[Dict[str, Any]]):
    """Выводит транзакции из JSON в консоль с маскировкой и форматированием."""
    if not transactions:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return
    print(f"Всего банковских операций в выборке: {len(transactions)}")
    for t in transactions:
        date = get_date(t.get('date', ''))
        desc = t.get('description', '')
        amount = t.get('operationAmount', {}).get('amount')
        valuta = t.get('operationAmount', {}).get('currency', {}).get('code')

        from_field = t.get('from', '')
        masked_from = mask_account_card(from_field) if from_field else ''

        to_field = t.get('to', '')
        masked_to = mask_account_card(to_field) if to_field else ''

        if masked_from and masked_to:
            print(f"{date} {desc}\n{masked_from} -> {masked_to}\nСумма: {amount} {valuta}")
        elif masked_from:
            print(f"{date} {desc}\n{masked_from}\nСумма: {amount} {valuta}")
        elif masked_to:
            print(f"{date} {desc}\n{masked_to}\nСумма: {amount} {valuta}")
        else:
            print(f"{date} {desc}\nСумма: {amount} {valuta}")


def main():
    print("Программа: Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    choice = input("Пользователь: ")
    file_path = input("Программа: Введите путь к файлу: ")

    try:
        if choice == '1':
            print("Программа: Для обработки выбран JSON-файл.")
            data = load_json_data(file_path)
        elif choice == '2':
            print("Программа: Для обработки выбран CSV-файл.")
            data = load_csv_data(file_path)
        elif choice == '3':
            print("Программа: Для обработки выбран XLSX-файл.")
            data = load_xlsx_data(file_path)
        else:
            print("Программа: Неверный выбор. Завершение работы.")
            return
    except Exception as e:
        print(f"Программа: Ошибка при загрузке файла: {e}")
        return
    while True:
        print("Программа: Введите статус, по которому необходимо выполнить фильтрацию.")
        print("Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING")
        status = input("Пользователь: ").strip().upper()
        try:
            filtered_data = filter_by_status(data, status)
            print(f"Программа: Операции отфильтрованы по статусу \"{status.upper()}\"")
            break
        except ValueError as e:
            print(f"Программа: {e}")
    sort_choice = input("Программа: Отсортировать операции по дате? Да/Нет\nПользователь: ").lower()
    if sort_choice == 'да':
        order = input("Программа: Отсортировать по возрастанию или по убыванию?\nПользователь: ").lower()
        ascending = 'возрастанию' in order
        filtered_data = sort_by_date(filtered_data, ascending)

    ruble_choice = input("Программа: Выводить только рублевые транзакции? Да/Нет\nПользователь: ").lower()
    if ruble_choice == 'да' and choice == '1':
        filtered_data = filter_ruble_transactions_json(filtered_data)
    else:
        filtered_data = filter_ruble_transactions(filtered_data)

    search_choice = input("Программа: Отфильтровать список транзакций по определенному слову в описании? Да/Нет\nПользователь: ").lower()
    if search_choice == 'да':
        search_term = input("Программа: Введите слово для поиска:\nПользователь: ")
        filtered_data = process_bank_search(filtered_data, search_term)

    print("Программа: Распечатываю итоговый список транзакций...")
    if choice == '1':
        print_transactions_json(filtered_data)
    else:
        print_transactions(filtered_data)


if __name__ == "__main__":
    main()
