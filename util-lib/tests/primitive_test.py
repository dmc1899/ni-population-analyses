"""
Tests for the primitive module.
"""
import unittest
from typing import Dict

import pytest

from util_lib.primitive import (
    source_target_list_to_dict,
    create_me_a_dict_of_using,
    remove_timestamp,
)


def test_basic_conversion() -> None:
    list_items = [
        {"source": "A", "target": "1"},
        {"source": "B", "target": "2"},
        {"source": "C", "target": "3"},
    ]
    expected_output = {"A": "1", "B": "2", "C": "3"}
    assert source_target_list_to_dict(list_items) == expected_output


def test_empty_list() -> None:
    list_items: list = []
    expected_output: Dict = {}
    print(source_target_list_to_dict(list_items))
    assert source_target_list_to_dict(list_items) == expected_output


def test_duplicate_sources() -> None:
    list_items = [{"source": "A", "target": "1"}, {"source": "A", "target": "2"}]
    expected_output = {"A": "2"}  # Last one should win
    assert source_target_list_to_dict(list_items), expected_output


def test_multiple_sources_and_targets() -> None:
    list_items = [
        {"source": "X", "target": "10"},
        {"source": "Y", "target": "20"},
        {"source": "Z", "target": "30"},
        {"source": "X", "target": "40"},  # Last one should win
    ]
    expected_output = {"X": "40", "Y": "20", "Z": "30"}
    assert source_target_list_to_dict(list_items) == expected_output


def test_single_item_list() -> None:
    list_items = [{"source": "A", "target": "1"}]
    expected_output = {"A": "1"}
    assert source_target_list_to_dict(list_items) == expected_output


def test_sources_with_none_values() -> None:
    list_items = [{"source": "A", "target": None}, {"source": "B", "target": "2"}]
    expected_output = {"A": None, "B": "2"}
    assert source_target_list_to_dict(list_items) == expected_output


def test_sources_with_empty_strings() -> None:
    list_items = [{"source": "", "target": "empty"}, {"source": "B", "target": "2"}]
    expected_output = {"": "empty", "B": "2"}
    assert source_target_list_to_dict(list_items) == expected_output


def test_empty_source() -> None:
    source: list = []
    result: Dict = create_me_a_dict_of_using(0, 1, source)
    assert not result


def test_invalid_key_value() -> None:
    source = [("Alice", 20, "A"), ("Bob", 22, "B")]
    try:
        create_me_a_dict_of_using(3, 4, source)
        assert False, "Expected IndexError to be raised"
    except IndexError:
        pass


def test_valid_input() -> None:
    source = [("Alice", 20, "A"), ("Bob", 22, "B"), ("Charlie", 19, "C")]
    result = create_me_a_dict_of_using(0, 2, source)
    expected = {"Alice": "A", "Bob": "B", "Charlie": "C"}
    assert result == expected


def test_different_key_value() -> None:
    source = [("Alice", 20, "A"), ("Bob", 22, "B"), ("Charlie", 19, "C")]
    result = create_me_a_dict_of_using(2, 1, source)
    expected = {"A": 20, "B": 22, "C": 19}
    assert result == expected


def test_valid_datetime_string() -> None:
    date_string = "2024-07-31 14:30:00"
    expected_output = "2024-07-31"
    assert remove_timestamp(date_string) == expected_output


def test_datetime_string_with_midnight() -> None:
    date_string = "2024-07-31 00:00:00"
    expected_output = "2024-07-31"
    assert remove_timestamp(date_string) == expected_output


def test_invalid_datetime_format() -> None:
    invalid_date_string = "2024-07-31T14:30:00"
    with pytest.raises(ValueError):
        remove_timestamp(invalid_date_string)


def test_invalid_input() -> None:
    invalid_input = "Not a date"
    with pytest.raises(ValueError):
        remove_timestamp(invalid_input)


def test_empty_string() -> None:
    empty_string = ""
    with pytest.raises(ValueError):
        remove_timestamp(empty_string)

