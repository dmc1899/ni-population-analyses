"""
 Convenience functions for primitive operations.
"""

from datetime import datetime
from typing import Dict, Any

import logging

logger = logging.getLogger(__name__)


# TODO DMcC - Can this function be combined with the function below?
def source_target_list_to_dict(list_dicts: list[Dict[str, Any]]) -> Dict[Any, Any]:
    """
    This function source_target_list_to_dict maps the
    'source' values to the 'target' values from a list of dictionaries,
    where each dictionary has a 'source' and 'target' key.
    For example, given this input:
        list_items = [
            {'source': 'A', 'target': '1'},
            {'source': 'B', 'target': '2'},
            {'source': 'C', 'target': '3'}
            ]
        the function returns:
        {
            'A': '1',
            'B': '2',
            'C': '3'
        }
    :param list_dicts:
    :return:
    """
    column_name_dict = {}
    for source_target_item in list_dicts:
        column_name_dict[source_target_item["source"]] = source_target_item["target"]

    return column_name_dict


def create_me_a_dict_of_using(
    key: str, value: str, source: list[Dict[str, Any]]
) -> Dict[Any, Any]:
    """
    This function creates a dictionary from a list of dictionaries,
    using the specified key and value from each dictionary.
    For example, given this input:
        key = 'name'
        value = 'age'
        source = [{'name': 'Alice', 'age': 25}, {'name': 'Bob', 'age': 30}]
    :param key: The list item to use as the key
    :param value: The list item to use as the value
    :param source: The list
    :return: Dictionary.
    """
    dict_item = {}
    for item in source:
        dict_item[item[key]] = item[value]

    return dict_item


def remove_timestamp(date_string: str) -> str:
    return str(datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S").date())
