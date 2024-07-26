import pandas as pd

pd.set_option('future.no_silent_downcasting', True)


def mutate_safely(function):
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
    def mutate(df, **params):
        tmp_df = df.copy()
        function(tmp_df, **params)
        return tmp_df
    return mutate


@mutate_safely
def fill_zeros(df, column) -> pd.DataFrame:
    """
    Walks through a pandas dataframe column and sets any zero values to the previous non-zero value in the column.

    Args:
        df (pandas.DataFrame): The dataframe to modify.
        column (str): The name of the column to modify.

    Returns:
        A new dataframe with forward-filled values in
        the column.
    """
    df[column] = df[column].infer_objects().replace(0, pd.NA).ffill().fillna(0)
    return df


@mutate_safely
def convert_obj_to_string(df):
    object_columns = list(df.select_dtypes(include='object').columns)

    for object_column in object_columns:
        df[object_column] = df[object_column].astype(str)

    return df


if __name__ == "__main__":

    data = {'col1': [1, 0, 0, 4, 5, 0, 0, 0, 9]}
    df = pd.DataFrame(data)
    expected_data = {'col1': [1, 1, 1, 4, 5, 5, 5, 5, 9]}
    expected_df = pd.DataFrame(expected_data)
# else:
#     print("File one executed when imported")
#
# if __name__ == "main":

    result_df = fill_zeros(df, 'col1')
    print(result_df)