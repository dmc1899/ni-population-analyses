import unittest
from util_lib.primitive import source_target_list_to_dict


def test_basic_conversion():
    list_items = [
        {'source': 'A', 'target': '1'},
        {'source': 'B', 'target': '2'},
        {'source': 'C', 'target': '3'}
    ]
    expected_output = {
        'A': '1',
        'B': '2',
        'C': '3'
    }
    assert source_target_list_to_dict(list_items) == expected_output


def test_empty_list():
    list_items = []
    expected_output = {}
    print("helloooooo")
    print(source_target_list_to_dict(list_items))
    assert source_target_list_to_dict(list_items) == expected_output


def test_duplicate_sources():
    list_items = [
        {'source': 'A', 'target': '1'},
        {'source': 'A', 'target': '2'}
    ]
    expected_output = {
        'A': '2'  # Last one should win
    }
    assert source_target_list_to_dict(list_items), expected_output


def test_multiple_sources_and_targets():
    list_items = [
        {'source': 'X', 'target': '10'},
        {'source': 'Y', 'target': '20'},
        {'source': 'Z', 'target': '30'},
        {'source': 'X', 'target': '40'}  # Last one should win
    ]
    expected_output = {
        'X': '40',
        'Y': '20',
        'Z': '30'
    }
    assert source_target_list_to_dict(list_items) == expected_output


def test_single_item_list():
    list_items = [
        {'source': 'A', 'target': '1'}
    ]
    expected_output = {
        'A': '1'
    }
    assert source_target_list_to_dict(list_items) == expected_output


def test_sources_with_none_values():
    list_items = [
        {'source': 'A', 'target': None},
        {'source': 'B', 'target': '2'}
    ]
    expected_output = {
        'A': None,
        'B': '2'
    }
    assert source_target_list_to_dict(list_items) == expected_output


def test_sources_with_empty_strings():
    list_items = [
        {'source': '', 'target': 'empty'},
        {'source': 'B', 'target': '2'}
    ]
    expected_output = {
        '': 'empty',
        'B': '2'
    }
    assert source_target_list_to_dict(list_items) == expected_output


if __name__ == '__main__':
    unittest.main()
