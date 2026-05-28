import csv
from typing import Dict
from typing import List

import pandas as pd


def read_csv_transactions(file_path: str) -> List[Dict]:
    """
    Считывает финансовые операции из CSV-файла.

    Args:
        file_path (str): Путь к CSV-файлу.

    Returns:
        List[Dict]: Список словарей с транзакциями.

    Raises:
        FileNotFoundError: Если файл не найден.
        Exception: При ошибках чтения файла.
    """
    try:
        transactions = []
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                transactions.append(row)
        return transactions
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл {file_path} не найден.")
    except Exception as e:
        raise Exception(f"Ошибка при чтении CSV-файла: {e}")


def read_excel_transactions(file_path: str) -> List[Dict]:
    """
    Считывает финансовые операции из Excel-файла.

    Args:
        file_path (str): Путь к Excel-файлу.

    Returns:
        List[Dict]: Список словарей с транзакциями.

    Raises:
        FileNotFoundError: Если файл не найден.
        Exception: При ошибках чтения файла.
    """
    try:
        df = pd.read_excel(file_path)
        transactions = df.to_dict('records')
        return transactions
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл {file_path} не найден.")
    except Exception as e:
        raise Exception(f"Ошибка при чтении Excel-файла: {e}")


# Чтение из CSV
csv_transactions = read_csv_transactions('C:/Users/lzspe/PycharmProjects/PythonProject1/transactions.csv')
print("Транзакции из CSV:")
for transaction in csv_transactions:
    print(transaction)

# Чтение из Excel
excel_transactions = read_excel_transactions('C:/Users/lzspe/PycharmProjects/PythonProject1/transactions_excel.xlsx')
print("\nТранзакции из Excel:")
for transaction in excel_transactions:
    print(transaction)
