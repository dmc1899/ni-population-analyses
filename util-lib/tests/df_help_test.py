import unittest

import pandas as pd

from util_lib import df_help


class TestFillZeros(unittest.TestCase):

    def test_fill_zeros_with_consecutive_zeros(self):
        input_data = {'col1': [1, 0, 0, 4, 5, 0, 0, 0, 9]}
        input_df = pd.DataFrame(input_data, dtype=object)

        expected_data = {'col1': [1, 1, 1, 4, 5, 5, 5, 5, 9]}
        expected_df = pd.DataFrame(expected_data, dtype=object)

        actual_df = df_help.fill_zeros(input_df, 'col1')

        pd.testing.assert_frame_equal(actual_df, expected_df)

    def test_fill_zeros_with_no_zeros(self):
        input_data = {'col1': [1, 2, 3, 4, 5]}
        input_df = pd.DataFrame(input_data, dtype=int)

        expected_data = {'col1': [1, 2, 3, 4, 5]}
        expected_df = pd.DataFrame(expected_data, dtype=int)

        actual_df = df_help.fill_zeros(input_df, 'col1')

        pd.testing.assert_frame_equal(actual_df, expected_df)

    def test_fill_zeros_with_all_zeros(self):
        input_data = {'col1': [0, 0, 0, 0, 0]}
        input_df = pd.DataFrame(input_data, dtype=object)

        expected_data = {'col1': [0, 0, 0, 0, 0]}
        expected_df = pd.DataFrame(expected_data, dtype=object)

        actual_df = df_help.fill_zeros(input_df, 'col1')

        pd.testing.assert_frame_equal(actual_df, expected_df)

    def test_fill_zeros_with_nan_values(self):
        input_data = {'col1': [1, pd.NA, 3, 0, pd.NA, 6, 0, 8]}
        input_df = pd.DataFrame(input_data, dtype=object)

        expected_data = {'col1': [1, 1, 3, 3, 3, 6, 6, 8]}
        expected_df = pd.DataFrame(expected_data, dtype=object)

        actual_df = df_help.fill_zeros(input_df, 'col1')

        pd.testing.assert_frame_equal(actual_df, expected_df)


if __name__ == '__main__':
    unittest.main()
