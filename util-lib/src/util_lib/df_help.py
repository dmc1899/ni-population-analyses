import pandas as pd


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
    pd.set_option('future.no_silent_downcasting', True)
    df_copy = df.copy(deep=True)
    print(df_copy.info(verbose=True))
    print(df_copy.info)
    # Replace zeros with NA
    df_copy[column] = df_copy[column].infer_objects().replace(0, pd.NA)
    print(df_copy.info(verbose=True))
    print(df_copy.info)
    print("about to ffill")
    # Perform forward fill to replace NA with the previous non-NA value
    df_copy[column] = df_copy[column].ffill().fillna(0)
    print(df_copy.info(verbose=True))
    print(df_copy.info)
    # print(df_copy)
    # # Infer better dtypes for object columns to avoid FutureWarning
    # # df_copy[column] = df_copy[column].infer_objects(copy=False)

    #df_copy[column] = df_copy[column].infer_objects(copy=False).replace(0, pd.NA).ffill() #fillna(method='ffill')

    return df_copy


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