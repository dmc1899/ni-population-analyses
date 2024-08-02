"""
Dataframe convenience functions for manipulation and validation.
"""

from typing import Dict, Callable, Any
import pandas as pd
from pandas import DataFrame

from util_lib.primitive import remove_timestamp
import logging

logger = logging.getLogger(__name__)

pd.set_option("future.no_silent_downcasting", True)


# TODO DMcC - Tigthen up type hints in the below function.
# def mutate_safely(function: Callable[[DataFrame, Mapping[str, Any]], None]) ->
# Callable[[DataFrame, Mapping[str, Any]], DataFrame]:
def mutate_safely(function: Callable) -> Any:
    """
    There are a limited number of pandas transformations that mutate the dataframe
    in place.  These are limited to modifying a column of data (insert, delete or update);
    assigning to the index or column attributes and modifying the values directly in the dataframe.

    The purpose of this function is to perform the mutating functions idempotently by mutating
    local deep copies of dataframes and returning new copies back to the caller.

    We use Python decorators to adopt this pattern without polluting our core functions. We
    decorate any function with @mutate_safely and write a function that mutates the given
    dataframe directly without returning it.
    """

    def mutate(input_df: DataFrame, **params: Any) -> DataFrame:
        tmp_df: DataFrame = input_df.copy()
        function(tmp_df, **params)
        return tmp_df

    return mutate


@mutate_safely
def fill_zeros(input_df: DataFrame, column: str) -> pd.DataFrame:
    """
    Walks through a pandas dataframe column and sets any zero values to the previous non-zero value in the column.

    Args:
        input_df (pandas.DataFrame): The dataframe to modify.
        column (str): The name of the column to modify.

    Returns:
        A new dataframe with forward-filled values in
        the column.
    """
    input_df[column] = (
        input_df[column].infer_objects().replace(0, pd.NA).ffill().fillna(0)
    )
    return input_df


@mutate_safely
def convert_obj_to_string(input_df: DataFrame) -> DataFrame:
    object_columns = list(input_df.select_dtypes(include="object").columns)

    for object_column in object_columns:
        input_df[object_column] = input_df[object_column].astype(str)

    return input_df


def read_worksheet_into_df(file_specification: Dict[str, str | int]) -> DataFrame:
    """
    Reads data from an Excel worksheet into a pandas DataFrame.

    Args:
        file_specification (Dict[str, str or int]): A dictionary containing the following keys:
            'dest_filepath' (str): The file path of the Excel file.
            'worksheet_name' (str): The name of the worksheet to read.
            'num_rows_from_top_to_ignore' (int, optional): The number of rows to skip from the top. Default is 0.
            'num_rows_to_read' (int, optional): The number of rows to read. Default is None (read all rows).
            'column_range_to_read' (str, optional): The range of columns to read. Default is None (read all columns).

    Returns:
        pd.DataFrame: A pandas DataFrame containing the data from the specified worksheet.

    Raises:
        FileNotFoundError: If the specified file path is invalid or the file does not exist.
        ValueError: If the specified worksheet name is invalid or the column range is invalid.
    """
    try:
        # Set default values for optional parameters
        num_rows_from_top_to_ignore: int = int(
            file_specification.get("num_rows_from_top_to_ignore", 0)
        )
        num_rows_to_read: int = int(file_specification.get("num_rows_to_read", 0))
        column_range_to_read: str = str(
            file_specification.get("column_range_to_read", "")
        )

        worksheet_df = pd.read_excel(
            file_specification["dest_filepath"],
            sheet_name=file_specification["worksheet_name"],
            skiprows=num_rows_from_top_to_ignore,
            header=0,
            nrows=num_rows_to_read,
            usecols=column_range_to_read,
        )
        return worksheet_df

    except FileNotFoundError as exc:
        raise FileNotFoundError(
            f"The file '{file_specification['dest_filepath']}' "
            f"does not exist or the path is invalid."
        ) from exc

    except ValueError as e:
        raise ValueError(
            f"Error reading worksheet '{file_specification['worksheet_name']}': {str(e)}"
        ) from e


def set_object_columns_to_string(input_df: DataFrame) -> DataFrame:
    df_to_process = input_df.copy()

    object_columns_list = list(df_to_process.select_dtypes(include="object").columns)

    for object_column in object_columns_list:
        df_to_process[object_column] = df_to_process[object_column].astype(str)

    return df_to_process


def rename_columns(input_df: DataFrame, column_mapping: Dict[str, str]) -> DataFrame:
    return input_df.rename(columns=column_mapping, inplace=False)


def inner_join_with(
    input_df: DataFrame,
    df_to_join: DataFrame,
    columns_to_include: list[str],
    join_key: str,
) -> DataFrame:
    return pd.merge(input_df, df_to_join[columns_to_include], on=join_key, how="inner")


@mutate_safely
def add_week_ending_date(
    input_df: DataFrame, default_date: str, existing_week_end_date_col_name: str
) -> None:

    def calculate_week_ending_date(
        week_ending: str, default: str = "2020-19-03"
    ) -> str:
        if week_ending == "19 Mar 2020 to 20 Mar 2020":
            return default

        if len(week_ending) > 10:
            return remove_timestamp(week_ending)

        return week_ending

    # Can be: Week Ends (Friday) or: Week_end_Date
    input_df["Week Ending Date"] = input_df[existing_week_end_date_col_name].apply(
        lambda raw_week_ending_date: calculate_week_ending_date(
            raw_week_ending_date, default_date
        )
    )


@mutate_safely
def convert_column_to_string(input_df: DataFrame, col_name: str) -> None:
    input_df[col_name] = input_df[col_name].astype(str)


def extract_only_this_year(input_df: DataFrame, rows_to_read: int) -> DataFrame:
    tmp_df = input_df[94:rows_to_read].reset_index(drop=True, inplace=False)
    assert (
        len(tmp_df) == 52
    ), "We must have a complete year of 52 registration weeks for 2022."
    return tmp_df


def extract_columns_of_interest(input_df: DataFrame) -> DataFrame:
    return input_df.iloc[0:, [0, 3]]


def convert_datatypes(input_df: DataFrame) -> DataFrame:
    return input_df.convert_dtypes()


@mutate_safely
def extract_and_cast_as_int(input_df: DataFrame, column: str) -> None:
    input_df[column] = (
        input_df[column]
        .astype(str)
        .str.replace("[a-zA-Z]", "", regex=True)
        .astype(float)
        .astype(int)
    )


if __name__ == "__main__":
    logger.info("main")
