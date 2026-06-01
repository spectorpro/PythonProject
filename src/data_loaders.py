import csv
import json
from typing import Any
from typing import Dict
from typing import List

import pandas as pd


def load_json_data(file_path: str) -> List[Dict[str, Any]]:
    """Загружает данные из JSON-файла."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_csv_data(file_path: str) -> List[Dict[str, Any]]:
    """Загружает данные из CSV-файла."""
    data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)
    return data


def load_xlsx_data(file_path: str) -> List[Dict[str, Any]]:
    """Загружает данные из XLSX-файла."""
    df = pd.read_excel(file_path)
    return df.to_dict('records')
