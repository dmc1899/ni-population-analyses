import unittest
import numpy as np
import pandas as pd

from util_lib import dataframe
from util_lib.dataframe import convert_obj_to_string


def test_fill_zeros_with_consecutive_zeros():
    input_data = {'col1': [1, 0, 0, 4, 5, 0, 0, 0, 9]}
    input_df = pd.DataFrame(input_data, dtype=object)

    expected_data = {'col1': [1, 1, 1, 4, 5, 5, 5, 5, 9]}
    expected_df = pd.DataFrame(expected_data, dtype=object)

    actual_df = dataframe.fill_zeros(df=input_df, column='col1')

    pd.testing.assert_frame_equal(actual_df, expected_df)


def test_fill_zeros_with_no_zeros():
    input_data = {'col1': [1, 2, 3, 4, 5]}
    input_df = pd.DataFrame(input_data, dtype=int)

    expected_data = {'col1': [1, 2, 3, 4, 5]}
    expected_df = pd.DataFrame(expected_data, dtype=int)

    actual_df = dataframe.fill_zeros(df=input_df, column='col1')

    pd.testing.assert_frame_equal(actual_df, expected_df)


def test_fill_zeros_with_all_zeros():
    input_data = {'col1': [0, 0, 0, 0, 0]}
    input_df = pd.DataFrame(input_data, dtype=object)

    expected_data = {'col1': [0, 0, 0, 0, 0]}
    expected_df = pd.DataFrame(expected_data, dtype=object)

    actual_df = dataframe.fill_zeros(df=input_df, column='col1')

    pd.testing.assert_frame_equal(actual_df, expected_df)


def test_fill_zeros_with_nan_values():
    input_data = {'col1': [1, pd.NA, 3, 0, pd.NA, 6, 0, 8]}
    input_df = pd.DataFrame(input_data, dtype=object)

    expected_data = {'col1': [1, 1, 3, 3, 3, 6, 6, 8]}
    expected_df = pd.DataFrame(expected_data, dtype=object)

    actual_df = dataframe.fill_zeros(df=input_df, column='col1')

    pd.testing.assert_frame_equal(actual_df, expected_df)


def test_all_object_columns():
    df = pd.DataFrame({
        'col1': ['a', 'b', 'c'],
        'col2': ['d', 'e', 'f']
    })
    result_df = convert_obj_to_string(df)

    for col in result_df.columns:
        assert result_df[col].dtype == 'object'
        assert(all(isinstance(val, str) for val in result_df[col]))


def test_mixed_columns():
    df = pd.DataFrame({
        'col1': ['a', 'b', 'c'],
        'col2': [1, 2, 3],
        'col3': [1.1, 2.2, 3.3]
    })
    result_df = convert_obj_to_string(df)

    assert result_df['col1'].dtype == 'object'
    assert(all(isinstance(val, str) for val in result_df['col1']))

    assert result_df['col2'].dtype == np.int64
    assert result_df['col3'].dtype == np.float64


def test_no_object_columns():
    df = pd.DataFrame({
        'col1': [1, 2, 3],
        'col2': [1.1, 2.2, 3.3]
    })
    result_df = convert_obj_to_string(df)

    assert result_df['col1'].dtype == np.int64
    assert result_df['col2'].dtype == np.float64


def test_empty_dataframe():
    df = pd.DataFrame()
    result_df = convert_obj_to_string(df)

    assert result_df.empty


def test_mixed_object_types():
    df = pd.DataFrame({
        'col1': ['a', 2, 'c'],
        'col2': [1.1, 'b', 3.3]
    })
    result_df = convert_obj_to_string(df)

    assert result_df['col1'].dtype == 'object'
    assert result_df['col2'].dtype == 'object'
    assert all(isinstance(val, str) for val in result_df['col1'])
    assert all(isinstance(val, str) for val in result_df['col2'])


if __name__ == '__main__':
    unittest.main()
