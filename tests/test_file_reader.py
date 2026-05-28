from unittest.mock import mock_open
from unittest.mock import patch

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


def test_read_csv_transactions_success(csv_content):
    with patch('builtins.open', mock_open(read_data=csv_content)):
        result = read_csv_transactions('dummy_path.csv')
        assert len(result) == 2
        assert result[0]['id'] == '1'
        assert result[0]['amount'] == '100.50'


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
