from unittest.mock import patch

import pandas as pd
import pytest

from src.file_reader import read_csv_transactions
from src.file_reader import read_excel_transactions


@pytest.fixture
def csv_content():
    return "id,amount,date\n1,100.50,2023-01-01\n2,200.75,2023-01-02"


@pytest.fixture
def excel_data():
    import pandas as pd
    return pd.DataFrame({
        'id': [1, 2],
        'amount': [100.50, 200.75],
        'date': ['2023-01-01', '2023-01-02']
    })


def test_read_csv_transactions_file_not_found():
    with pytest.raises(FileNotFoundError):
        read_csv_transactions('nonexistent.csv')


def test_read_excel_transactions_success(excel_data):
    with patch('pandas.read_excel', return_value=excel_data):
        result = read_excel_transactions('dummy_path.xlsx')
        assert len(result) == 2
        assert result[0]['id'] == 1
        assert result[0]['amount'] == 100.50


def test_read_excel_transactions_file_not_found():
    with patch('pandas.read_excel', side_effect=FileNotFoundError()):
        with pytest.raises(FileNotFoundError):
            read_excel_transactions('nonexistent.xlsx')


@pytest.fixture
def empty_csv_content():
    return "id,amount,date\n"


def test_read_csv_transactions_empty_file(empty_csv_content, tmp_path):
    """Тест чтения пустого CSV-файла (только заголовки)."""
    csv_file = tmp_path / "empty_transactions.csv"
    csv_file.write_text(empty_csv_content)

    result = read_csv_transactions(str(csv_file))
    assert len(result) == 0


@pytest.fixture
def excel_data_with_missing_values():
    import pandas as pd
    return pd.DataFrame({
        'id': [1, None],
        'amount': [100.50, None],
        'date': ['2023-01-01', '2023-01-02']
    })


def test_read_excel_transactions_with_missing_values(excel_data_with_missing_values):
    """Тест обработки Excel с пропущенными значениями."""
    with patch('pandas.read_excel', return_value=excel_data_with_missing_values):
        result = read_excel_transactions('dummy_path.xlsx')
        assert len(result) == 2

        # Проверяем корректные значения
        assert result[0]['id'] == 1
        assert result[0]['amount'] == 100.50

        # Проверяем пропущенные значения через pd.isna()
        assert pd.isna(result[1]['id'])
        assert pd.isna(result[1]['amount'])
