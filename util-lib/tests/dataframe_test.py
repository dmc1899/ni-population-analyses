"""
Tests for dataframe module.
"""

from pathlib import Path
import unittest
from typing import Dict

import numpy as np
import pandas as pd
import pytest
from pandas import DataFrame

from util_lib.dataframe import (
    convert_obj_to_string,
    read_worksheet_into_df,
    inner_join_with,
    fill_zeros,
    set_object_columns_to_string,
    rename_columns,
    add_week_ending_date,
    convert_column_to_string,
    extract_and_cast_as_int,
)

current_dir = Path(__file__).parent
resources_dir = current_dir / "resources"


def test_fill_zeros_with_consecutive_zeros() -> None:
    input_data = {"col1": [1, 0, 0, 4, 5, 0, 0, 0, 9]}
    input_df = pd.DataFrame(input_data, dtype=object)

    expected_data = {"col1": [1, 1, 1, 4, 5, 5, 5, 5, 9]}
    expected_df = pd.DataFrame(expected_data, dtype=object)

    actual_df = fill_zeros(input_df=input_df, column="col1")

    pd.testing.assert_frame_equal(actual_df, expected_df)


def test_fill_zeros_with_no_zeros() -> None:
    input_data = {"col1": [1, 2, 3, 4, 5]}
    input_df = pd.DataFrame(input_data, dtype=int)

    expected_data = {"col1": [1, 2, 3, 4, 5]}
    expected_df = pd.DataFrame(expected_data, dtype=int)

    actual_df = fill_zeros(input_df=input_df, column="col1")

    pd.testing.assert_frame_equal(actual_df, expected_df)


def test_fill_zeros_with_all_zeros() -> None:
    input_data = {"col1": [0, 0, 0, 0, 0]}
    input_df = pd.DataFrame(input_data, dtype=object)

    expected_data = {"col1": [0, 0, 0, 0, 0]}
    expected_df = pd.DataFrame(expected_data, dtype=object)

    actual_df = fill_zeros(input_df=input_df, column="col1")

    pd.testing.assert_frame_equal(actual_df, expected_df)


def test_fill_zeros_with_nan_values() -> None:
    input_data = {"col1": [1, pd.NA, 3, 0, pd.NA, 6, 0, 8]}
    input_df = pd.DataFrame(input_data, dtype=object)

    expected_data = {"col1": [1, 1, 3, 3, 3, 6, 6, 8]}
    expected_df = pd.DataFrame(expected_data, dtype=object)

    actual_df = fill_zeros(input_df=input_df, column="col1")

    pd.testing.assert_frame_equal(actual_df, expected_df)


def test_all_object_columns() -> None:
    df = pd.DataFrame({"col1": ["a", "b", "c"], "col2": ["d", "e", "f"]})
    result_df = convert_obj_to_string(df)

    for col in result_df.columns:
        assert result_df[col].dtype == "object"
        assert all(isinstance(val, str) for val in result_df[col])


def test_mixed_columns() -> None:
    df = pd.DataFrame(
        {"col1": ["a", "b", "c"], "col2": [1, 2, 3], "col3": [1.1, 2.2, 3.3]}
    )
    result_df = convert_obj_to_string(df)

    assert result_df["col1"].dtype == "object"
    assert all(isinstance(val, str) for val in result_df["col1"])

    assert result_df["col2"].dtype == np.int64
    assert result_df["col3"].dtype == np.float64


def test_no_object_columns() -> None:
    df = pd.DataFrame({"col1": [1, 2, 3], "col2": [1.1, 2.2, 3.3]})
    result_df = convert_obj_to_string(df)

    assert result_df["col1"].dtype == np.int64
    assert result_df["col2"].dtype == np.float64


def test_empty_dataframe() -> None:
    df = pd.DataFrame()
    result_df = convert_obj_to_string(df)

    assert result_df.empty


def test_mixed_object_types() -> None:
    df = pd.DataFrame({"col1": ["a", 2, "c"], "col2": [1.1, "b", 3.3]})
    result_df = convert_obj_to_string(df)

    assert result_df["col1"].dtype == "object"
    assert result_df["col2"].dtype == "object"
    assert all(isinstance(val, str) for val in result_df["col1"])
    assert all(isinstance(val, str) for val in result_df["col2"])


def test_read_present_worksheet() -> None:
    test_input_file = resources_dir / "dataframe_test" / "valid_workbook.xlsx"

    file_spec = {
        "dest_filepath": test_input_file,
        "worksheet_name": "Table 3",
        "num_rows_from_top_to_ignore": 3,
        "num_rows_to_read": 29,
        "column_range_to_read": "A:C",
    }

    df = read_worksheet_into_df(file_spec)
    assert isinstance(df, pd.DataFrame)
    assert df.shape == (29, 3)


def test_read_missing_worksheet() -> None:
    test_input_file = resources_dir / "dataframe_test" / "missing_workbook.xlsx"

    file_spec = {
        "dest_filepath": test_input_file,
        "worksheet_name": "Table 3",
        "num_rows_from_top_to_ignore": 3,
        "num_rows_to_read": 29,
        "column_range_to_read": "A:C",
    }

    with pytest.raises(FileNotFoundError) as read_error:
        read_worksheet_into_df(file_spec)
    assert "does not exist or the path is invalid" in str(read_error.value)


def test_with_object_columns() -> None:
    input_df = pd.DataFrame({"A": ["a", "b", "c"], "B": ["1", "2", "3"]})
    result_df = set_object_columns_to_string(input_df)
    expected_df = pd.DataFrame({"A": ["a", "b", "c"], "B": ["1", "2", "3"]})
    assert result_df.equals(expected_df)
    assert result_df.dtypes["A"] == "object"
    assert result_df.dtypes["B"] == "object"


def test_without_object_columns() -> None:
    input_df = pd.DataFrame({"A": [1, 2, 3], "B": [4.0, 5.0, 6.0]})
    result_df = set_object_columns_to_string(input_df)
    expected_df = input_df.copy()
    assert result_df.equals(expected_df)


def test_with_mixed_columns() -> None:
    input_df = pd.DataFrame(
        {"A": ["a", "b", "c"], "B": [1, 2, 3], "C": [4.0, 5.0, 6.0]}
    )
    result_df = set_object_columns_to_string(input_df)
    expected_df = pd.DataFrame(
        {"A": ["a", "b", "c"], "B": [1, 2, 3], "C": [4.0, 5.0, 6.0]}
    )
    assert result_df.equals(expected_df)
    assert result_df.dtypes["A"] == "object"
    assert result_df.dtypes["B"] == "int64"
    assert result_df.dtypes["C"] == "float64"


def test_valid_column_mapping() -> None:
    df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6], "C": [7, 8, 9]})
    column_mapping = {"A": "Alpha", "B": "Beta"}
    result_df = rename_columns(df, column_mapping)
    expected_df = pd.DataFrame({"Alpha": [1, 2, 3], "Beta": [4, 5, 6], "C": [7, 8, 9]})
    assert result_df.equals(expected_df)


def test_empty_column_mapping() -> None:
    df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
    column_mapping: Dict[str, str] = {}
    result_df: DataFrame = rename_columns(df, column_mapping)
    expected_df: DataFrame = df.copy()
    assert result_df.equals(expected_df)


def test_non_existing_columns_in_mapping() -> None:
    df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
    column_mapping = {"X": "Xeno", "Y": "Ypsilon"}
    result_df = rename_columns(df, column_mapping)
    expected_df = df.copy()
    assert result_df.equals(expected_df)


def test_partial_column_mapping() -> None:
    df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6], "C": [7, 8, 9]})
    column_mapping = {"B": "Beta"}
    result_df = rename_columns(df, column_mapping)
    expected_df = pd.DataFrame({"A": [1, 2, 3], "Beta": [4, 5, 6], "C": [7, 8, 9]})
    assert result_df.equals(expected_df)


def test_standard_inner_join() -> None:
    df = pd.DataFrame({"id": [1, 2, 3], "name": ["Alice", "Bob", "Charlie"]})
    df_to_join = pd.DataFrame(
        {
            "id": [1, 2, 4],
            "age": [25, 30, 22],
            "city": ["New York", "Los Angeles", "Chicago"],
        }
    )
    columns_to_include = ["id", "age"]
    join_key = "id"
    result_df = inner_join_with(df, df_to_join, columns_to_include, join_key)
    expected_df = pd.DataFrame(
        {"id": [1, 2], "name": ["Alice", "Bob"], "age": [25, 30]}
    )
    assert result_df.equals(expected_df)


def test_non_matching_keys() -> None:
    df = pd.DataFrame({"id": [1, 2, 3], "name": ["Alice", "Bob", "Charlie"]})
    df_to_join = pd.DataFrame(
        {
            "id": [4, 5, 6],
            "age": [25, 30, 35],
            "city": ["New York", "Los Angeles", "Chicago"],
        }
    )
    columns_to_include = ["id", "age"]
    join_key = "id"
    result_df = inner_join_with(df, df_to_join, columns_to_include, join_key)
    assert result_df.empty


def test_empty_dataframes() -> None:
    df = pd.DataFrame(columns=["id", "name"])
    df_to_join = pd.DataFrame(columns=["id", "age", "city"])
    columns_to_include = ["id", "age"]
    join_key = "id"
    result_df = inner_join_with(df, df_to_join, columns_to_include, join_key)
    expected_df = pd.DataFrame(columns=["id", "name", "age"])
    assert result_df.equals(expected_df)


def test_partial_column_inclusion() -> None:
    df = pd.DataFrame({"id": [1, 2, 3], "name": ["Alice", "Bob", "Charlie"]})
    df_to_join = pd.DataFrame(
        {
            "id": [1, 2, 3],
            "age": [25, 30, 35],
            "city": ["New York", "Los Angeles", "Chicago"],
        }
    )
    columns_to_include = ["id", "city"]
    join_key = "id"
    result_df = inner_join_with(df, df_to_join, columns_to_include, join_key)
    expected_df = pd.DataFrame(
        {
            "id": [1, 2, 3],
            "name": ["Alice", "Bob", "Charlie"],
            "city": ["New York", "Los Angeles", "Chicago"],
        }
    )
    assert result_df.equals(expected_df)


def _create_sample_df(data: list, column_name: str) -> DataFrame:
    return pd.DataFrame({column_name: data})


def test_add_week_ending_date_default_date() -> None:
    df = _create_sample_df(["19 Mar 2020 to 20 Mar 2020"], "Week Ends (Friday)")
    result = add_week_ending_date(
        input_df=df,
        default_date="2020-03-19",
        existing_week_end_date_col_name="Week Ends (Friday)",
    )
    assert result["Week Ending Date"].iloc[0] == "2020-03-19"


def test_add_week_ending_date_long_date() -> None:
    df = _create_sample_df(["2020-03-20 00:00:00"], "Week Ends (Friday)")
    result = add_week_ending_date(
        input_df=df,
        default_date="2020-03-19",
        existing_week_end_date_col_name="Week Ends (Friday)",
    )
    assert result["Week Ending Date"].iloc[0] == "2020-03-20"


def test_add_week_ending_date_short_date() -> None:
    df = _create_sample_df(["2020-03-20"], "Week Ends (Friday)")
    result = add_week_ending_date(
        input_df=df,
        default_date="2020-03-19",
        existing_week_end_date_col_name="Week Ends (Friday)",
    )
    assert result["Week Ending Date"].iloc[0] == "2020-03-20"


def test_add_week_ending_date_mixed_dates() -> None:
    df = _create_sample_df(
        ["19 Mar 2020 to 20 Mar 2020", "2020-03-27 00:00:00", "2020-04-03"],
        "Week_end_Date",
    )
    result = add_week_ending_date(
        input_df=df,
        default_date="2020-03-19",
        existing_week_end_date_col_name="Week_end_Date",
    )
    assert result["Week Ending Date"].tolist() == [
        "2020-03-19",
        "2020-03-27",
        "2020-04-03",
    ]


def test_add_week_ending_date_empty_dataframe() -> None:
    df = pd.DataFrame()
    with pytest.raises(KeyError):
        add_week_ending_date(
            input_df=df,
            default_date="2020-03-19",
            existing_week_end_date_col_name="Week Ends (Friday)",
        )


def test_add_week_ending_date_missing_column() -> None:
    df = _create_sample_df(["2020-03-20"], "Wrong Column Name")
    with pytest.raises(KeyError):
        add_week_ending_date(
            input_df=df,
            default_date="2020-03-19",
            existing_week_end_date_col_name="Week Ends (Friday)",
        )


def test_add_week_ending_date_different_column_names() -> None:
    df = _create_sample_df(["2020-03-20"], "Custom Column")
    result = add_week_ending_date(
        input_df=df,
        default_date="2020-03-19",
        existing_week_end_date_col_name="Custom Column",
    )
    assert result["Week Ending Date"].iloc[0] == "2020-03-20"


def test_add_week_ending_date_invalid_date_format() -> None:
    df = _create_sample_df(["Invalid Date"], "Week Ends (Friday)")

    with pytest.raises(ValueError) as value_error:
        add_week_ending_date(
            input_df=df,
            default_date="2020-03-19",
            existing_week_end_date_col_name="Week Ends (Friday)",
        )
        assert " does not match format" in str(value_error.value)


def test_convert_int_column_to_string() -> None:
    input_df = pd.DataFrame({"A": [1, 2, 3], "B": [4.0, 5.0, 6.0]})

    assert input_df["A"].dtype == np.int64

    actual_df = convert_column_to_string(input_df=input_df, col_name="A")
    assert actual_df["A"].dtype == np.object_


def test_convert_float_column_to_string() -> None:
    input_df = pd.DataFrame({"A": [1, 2, 3], "B": [4.1, 5.2, 6.3]})
    assert input_df["B"].dtype == np.float64
    actual_df = convert_column_to_string(input_df=input_df, col_name="B")
    assert actual_df["B"].dtype == np.object_


def test_non_existent_column() -> None:
    df = pd.DataFrame({"A": [1, 2, 3], "B": [4.1, 5.2, 6.3]})
    with pytest.raises(KeyError):
        convert_column_to_string(input_df=df, col_name="C")


def test_already_string_column() -> None:
    df = pd.DataFrame({"A": ["apple", "banana", "cherry"], "B": [1, 2, 3]})
    actual_df = convert_column_to_string(input_df=df, col_name="A")
    expected_df = pd.DataFrame({"A": ["apple", "banana", "cherry"], "B": [1, 2, 3]})
    assert actual_df.equals(expected_df)
    assert df["A"].dtype == object


def test_extract_and_cast_as_int_numeric_strings() -> None:
    df = pd.DataFrame({"col": ["123", "456", "789"]})
    result = extract_and_cast_as_int(input_df=df, column="col")
    assert result["col"].tolist() == [123, 456, 789]
    assert result["col"].dtype == np.int64


def test_extract_and_cast_as_int_mixed_strings() -> None:
    df = pd.DataFrame({"col": ["abc123", "456def", "ghi789jkl"]})
    result = extract_and_cast_as_int(input_df=df, column="col")
    assert result["col"].tolist() == [123, 456, 789]


def test_extract_and_cast_as_int_float_strings() -> None:
    df = pd.DataFrame({"col": ["123.45", "456.78", "789.01"]})
    result = extract_and_cast_as_int(input_df=df, column="col")
    assert result["col"].tolist() == [123, 456, 789]


def test_extract_and_cast_as_int_mixed_types() -> None:
    df = pd.DataFrame({"col": [123, "456", 789.0, "abc101"]})
    result = extract_and_cast_as_int(input_df=df, column="col")
    assert result["col"].tolist() == [123, 456, 789, 101]


def test_extract_and_cast_as_int_empty_strings() -> None:
    df = pd.DataFrame({"col": ["", "abc", "123"]})
    with pytest.raises(ValueError):
        extract_and_cast_as_int(input_df=df, column="col")


def test_extract_and_cast_as_int_non_existent_column() -> None:
    df = pd.DataFrame({"col": [123, 456, 789]})
    with pytest.raises(KeyError):
        extract_and_cast_as_int(input_df=df, column="non_existent_column")


def test_extract_and_cast_as_int_preserve_other_columns() -> None:
    df = pd.DataFrame(
        {"col1": ["abc123", "456def", "ghi789jkl"], "col2": ["x", "y", "z"]}
    )
    result = extract_and_cast_as_int(input_df=df, column="col1")
    assert result["col1"].tolist() == [123, 456, 789]
    assert result["col2"].tolist() == ["x", "y", "z"]


def test_extract_and_cast_as_int_negative_numbers() -> None:
    df = pd.DataFrame({"col": ["-123", "abc-456", "-789def"]})
    result = extract_and_cast_as_int(input_df=df, column="col")
    assert result["col"].tolist() == [-123, -456, -789]


def test_extract_and_cast_as_int_zero_values() -> None:
    df = pd.DataFrame({"col": ["000", "abc000", "000def"]})
    result = extract_and_cast_as_int(input_df=df, column="col")
    assert result["col"].tolist() == [0, 0, 0]

