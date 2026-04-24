import pytest
from src.processing import filter_by_state, sort_by_date
from datetime import datetime, timedelta
from typing import List, Dict, Any


@pytest.fixture
def basic_sample_data() -> List[Dict[str, Any]]:
    """Базовый набор данных с разными статусами и датами."""
    base_date = datetime(2023, 1, 1)
    return [
        {'id': 1, 'state': 'EXECUTED', 'amount': 100, 'date': base_date},
        {'id': 2, 'state': 'PENDING', 'amount': 200, 'date': base_date + timedelta(days=1)},
        {'id': 3, 'state': 'CANCELED', 'amount': 50, 'date': base_date + timedelta(days=2)},
        {'id': 4, 'state': 'EXECUTED', 'amount': 300, 'date': base_date + timedelta(days=3)},
        {'id': 5, 'state': 'FAILED', 'amount': 75, 'date': base_date + timedelta(days=4)},
    ]


@pytest.fixture
def empty_data() -> List:
    """Пустой список данных."""
    return []


@pytest.fixture
def data_without_executed() -> List[Dict[str, Any]]:
    """Данные без статуса EXECUTED."""
    base_date = datetime(2023, 2, 1)
    return [
        {'id': 6, 'state': 'PENDING', 'amount': 150, 'date': base_date},
        {'id': 7, 'state': 'CANCELED', 'amount': 25, 'date': base_date + timedelta(days=1)},
    ]


@pytest.fixture
def data_with_missing_state() -> List[Dict[str, Any]]:
    """Данные с отсутствующим ключом 'state' у некоторых записей."""
    base_date = datetime(2023, 3, 1)
    return [
        {'id': 8, 'amount': 400, 'date': base_date},  # Нет ключа 'state'
        {'id': 9, 'state': None, 'amount': 500, 'date': base_date + timedelta(days=1)},  # state = None
        {'id': 10, 'state': 'EXECUTED', 'amount': 600, 'date': base_date + timedelta(days=2)},
    ]


@pytest.fixture
def data_with_duplicate_states() -> List[Dict[str, Any]]:
    """Данные с повторяющимися статусами и разными датами."""
    base_date = datetime(2023, 4, 1)
    return [
        {'id': 11, 'state': 'EXECUTED', 'amount': 1000, 'date': base_date},
        {'id': 12, 'state': 'EXECUTED', 'amount': 1500, 'date': base_date + timedelta(days=5)},
        {'id': 13, 'state': 'PENDING', 'amount': 800, 'date': base_date + timedelta(days=10)},
        {'id': 14, 'state': 'EXECUTED', 'amount': 1200, 'date': base_date + timedelta(days=15)},
    ]


@pytest.fixture
def data_with_edge_cases() -> List[Dict[str, Any]]:
    """Крайние случаи: пустые строки, None, специальные символы в статусах"""
    base_date = datetime(2023, 5, 1)
    return [
        {'id': 15, 'state': '', 'amount': 0, 'date': base_date},  # Пустой статуc
        {'id': 16, 'state': ' ', 'amount': 10, 'date': base_date + timedelta(days=1)},  # Пробел
        {'id': 17, 'state': None, 'amount': 20, 'date': base_date + timedelta(days=2)},  # None
        {'id': 18, 'state': 'SOME-STATE_WITH-SYMBOLS!@#', 'amount': 30, 'date': base_date + timedelta(days=3)},  # Спецсимволы
        {'id': 19, 'state': 'executed', 'amount': 40, 'date': base_date + timedelta(days=4)},  # Разные регистры
    ]


@pytest.fixture
def data_with_various_dates() -> List[Dict[str, Any]]:
    """Данные с широким диапазоном дат для проверки временной фильтрации."""
    start_date = datetime(2022, 12, 1)
    return [
        {'id': 20, 'state': 'EXECUTED', 'amount': 500, 'date': start_date},
        {'id': 21, 'state': 'PENDING', 'amount': 600, 'date': start_date + timedelta(days=30)},
        {'id': 22, 'state': 'CANCELED', 'amount': 700, 'date': start_date + timedelta(days=60)},
        {'id': 23, 'state': 'EXECUTED', 'amount': 800, 'date': start_date + timedelta(days=90)},
        {'id': 24, 'state': 'FAILED', 'amount': 900, 'date': start_date + timedelta(days=120)},
    ]


@pytest.fixture
def complex_data_mix() -> List[Dict[str, Any]]:
    """Сложный микс: разные статусы, даты, пропущенные поля."""
    base_date = datetime(2023, 6, 1)
    return [
        {'id': 25, 'state': 'EXECUTED', 'amount': 1000, 'date': base_date, 'category': 'A'},
        {'id': 26, 'state': 'PENDING', 'amount': 1100, 'date': base_date + timedelta(days=7), 'category': 'B'},
        {'id': 27, 'amount': 1200, 'date': base_date + timedelta(days=14)},  # Нет state
        {'id': 28, 'state': 'CANCELED', 'date': base_date + timedelta(days=21), 'category': 'C'},  # Нет amount
        {'id': 29, 'state': 'EXECUTED', 'amount': 1300, 'category': 'D'},  # Нет date
        {'id': 30, 'state': None, 'amount': 1400, 'date': base_date + timedelta(days=28)},  # state = None
    ]


# Параметризованные тесты
@pytest.mark.parametrize("test_state,expected_count", [
    ('EXECUTED', 2),
    ('PENDING', 1),
    ('CANCELED', 1),
    ('FAILED', 1),
    ('UNKNOWN', 0),  # Статус, которого нет в данных
    ('', 0),        # Пустой статус
    (' ', 0),       # Пробел как статус
])
def test_filter_by_state_parametrized(
    basic_sample_data: List[Dict[str, Any]],
    test_state: str,
    expected_count: int
) -> None:
    """Тестирование фильтрации для различных статусов (включая отсутствующие)."""
    result = filter_by_state(basic_sample_data, test_state)
    assert len(result) == expected_count
    if expected_count > 0:
        assert all(item['state'] == test_state for item in result)


def test_filter_default_state(basic_sample_data: List[Dict[str, Any]]) -> None:
    """Тестирование фильтрации с состоянием по умолчанию."""
    result = filter_by_state(basic_sample_data)
    assert len(result) == 2
    assert all(item['state'] == 'EXECUTED' for item in result)
    assert result[0]['id'] == 1
    assert result[1]['id'] == 4


def test_filter_specific_state(basic_sample_data: List[Dict[str, Any]]) -> None:
    """Тестирование фильтрации по конкретному статусу."""
    result = filter_by_state(basic_sample_data, 'PENDING')
    assert len(result) == 1
    assert result[0]['state'] == 'PENDING'
    assert result[0]['amount'] == 200
    assert result[0]['date'] == datetime(2023, 1, 2)


def test_no_matching_state(data_without_executed: List[Dict[str, Any]]) -> None:
    """Тестирование случая, когда нет записей с указанным статусом."""
    result = filter_by_state(data_without_executed, 'EXECUTED')
    assert len(result) == 0
    assert result == []


def test_empty_input_list(empty_data: List[Dict[str, Any]]) -> None:
    """Тестирование с пустым входным списком."""
    result = filter_by_state(empty_data, 'EXECUTED')
    assert len(result) == 0
    assert result == []


def test_missing_state_key(data_with_missing_state: List[Dict[str, Any]]) -> None:
    """Тестирование данных, где у некоторых записей нет ключа 'state'."""
    result = filter_by_state(data_with_missing_state, 'EXECUTED')
    # Должны быть только записи с state == 'EXECUTED', остальные игнорируются
    assert len(result) == 1
    assert result[0]['state'] == 'EXECUTED'
    assert result[0]['id'] == 10


def test_duplicate_states(data_with_duplicate_states: List[Dict[str, Any]]) -> None:
    """Тестирование данных с повторяющимися статусами."""
    result = filter_by_state(data_with_duplicate_states, 'EXECUTED')
    assert len(result) == 3
    assert all(item['state'] == 'EXECUTED' for item in result)
    # Проверяем, что все записи с EXECUTED найдены
    executed_ids = [item['id'] for item in result]
    assert sorted(executed_ids) == [11, 12, 14]


def test_edge_cases_states(data_with_edge_cases: List[Dict[str, Any]]) -> None:
    """Тестирование крайних случаев статусов."""
    # Тест для пустого статуса
    empty_result = filter_by_state(data_with_edge_cases, '')
    assert len(empty_result) == 1
    assert empty_result[0]['state'] == ''

    # Тест для статуса с пробелом
    space_result = filter_by_state(data_with_edge_cases, ' ')
    assert len(space_result) == 1
    assert space_result[0]['state'] == ' '

    # Тест для регистра (должен быть точный матч)
    case_result = filter_by_state(data_with_edge_cases, 'executed')
    assert len(case_result) == 1
    assert case_result[0]['state'] == 'executed'


def test_date_preservation(basic_sample_data: List[Dict[str, Any]]) -> None:
    """Проверка, что даты сохраняются корректно при фильтрации."""
    result = filter_by_state(basic_sample_data, 'FAILED')
    assert len(result) == 1
    assert result[0]['date'] == datetime(2023, 1, 5)
    assert isinstance(result[0]['date'], datetime)


def test_complex_data_mix_filtering(complex_data_mix: List[Dict[str, Any]]) -> None:
    """Тестирование сложной комбинации данных с пропущенными полями."""
    result = filter_by_state(complex_data_mix, 'EXECUTED')
    assert len(result) == 2

    # Проверяем первую запись EXECUTED
    executed1 = result[0]
    assert executed1['id'] == 25
    assert executed1['state'] == 'EXECUTED'
    assert executed1['amount'] == 1000
    assert 'category' in executed1

    # Проверяем вторую запись EXECUTED (без даты)
    executed2 = result[1]
    assert executed2['id'] == 29
    assert executed2['state'] == 'EXECUTED'
    assert executed2['amount'] == 1300
    assert 'date' not in executed2  # Дата отсутствует в исходной записи


def test_multiple_filters_consistency(basic_sample_data: List[Dict[str, Any]]) -> None:
    """Проверка консистентности при последовательных вызовах с разными статусами."""
    states_to_test: List[str] = ['EXECUTED', 'PENDING', 'CANCELED', 'FAILED']
    total_found: int = 0

    for state in states_to_test:
        result = filter_by_state(basic_sample_data, state)
        total_found += len(result)
        # Каждый результат должен содержать только указанный статус
        if result:
            assert all(item['state'] == state for item in result)

    # Общее количество найденных записей должно соответствовать размеру исходных данных
    # минус записи без 'state' или с None (если бы они были в basic_sample_data)
    assert total_found == len(basic_sample_data)


@pytest.fixture
def sample_data() -> List[Dict[str, Any]]:
    """Базовый набор данных с разными датами."""
    return [
        {'id': 1, 'date': '2023-01-15T10:30:00', 'state': 'active'},
        {'id': 2, 'date': '2023-03-20T14:15:00', 'state': 'inactive'},
        {'id': 3, 'date': '2022-12-01T09:45:00', 'state': 'pending'},
        {'id': 4, 'date': '2023-02-10T16:20:00', 'state': 'completed'},
    ]


@pytest.fixture
def data_with_same_dates() -> List[Dict[str, Any]]:
    """Данные с одинаковыми датами для проверки стабильности сортировки."""
    return [
        {'id': 1, 'date': '2023-01-15T10:30:00', 'state': 'active'},
        {'id': 2, 'date': '2023-01-15T10:30:00', 'state': 'inactive'},
        {'id': 3, 'date': '2023-01-15T10:30:00', 'state': 'pending'},
    ]


@pytest.fixture
def data_with_z_suffix() -> List[Dict[str, Any]]:
    """Данные с датами в формате ISO с суффиксом Z (UTC)."""
    return [
        {'id': 1, 'date': '2023-01-15T10:30:00Z', 'state': 'active'},
        {'id': 2, 'date': '2023-03-20T14:15:00Z', 'state': 'inactive'},
        {'id': 3, 'date': '2022-12-01T09:45:00Z', 'state': 'pending'},
    ]


def test_sort_ascending(sample_data: List[Dict[str, Any]]) -> None:
    """Тест сортировки по возрастанию дат."""
    result = sort_by_date(sample_data, reverse=False)
    dates = [item['date'] for item in result]
    expected_dates = [
        '2022-12-01T09:45:00',
        '2023-01-15T10:30:00',
        '2023-02-10T16:20:00',
        '2023-03-20T14:15:00'
    ]
    assert dates == expected_dates


def test_same_dates_stability(data_with_same_dates: List[Dict[str, Any]]) -> None:
    """Тест стабильности сортировки при одинаковых датах."""
    original_order = [item['id'] for item in data_with_same_dates]
    result = sort_by_date(data_with_same_dates)
    result_order = [item['id'] for item in result]
    # При одинаковых датах порядок должен сохраняться (стабильная сортировка)
    assert result_order == original_order


def test_z_suffix_handling(data_with_z_suffix: List[Dict[str, Any]]) -> None:
    """Тест обработки дат с суффиксом Z (UTC)."""
    result = sort_by_date(data_with_z_suffix)
    dates = [item['date'] for item in result]
    expected_dates = [
        '2023-03-20T14:15:00Z',
        '2023-01-15T10:30:00Z',
        '2022-12-01T09:45:00Z'
    ]
    assert dates == expected_dates
