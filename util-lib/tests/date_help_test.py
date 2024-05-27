import logging
import unittest

from util_lib import date_help

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


class TestReverseDateFormat(unittest.TestCase):

    def test_valid_date_only_succeeds(self) -> None:
        input_date = "31-12-2023"
        expected_output = "2023-12-31"
        actual_output = date_help.reformat_date(input_date)
        LOGGER.info("Returned: %s", actual_output)
        self.assertEqual(actual_output, expected_output)

    def test_valid_date_time_only_succeeds(self) -> None:
        given_input = "12/11/2018 09:15:32"
        given_input_format = "%d/%m/%Y %H:%M:%S"

        expected_output = "2018-11-12"

        actual_output = date_help.reformat_date(given_input, given_input_format)
        LOGGER.info("Returned: %s", actual_output)

        self.assertEqual(actual_output, expected_output)


if __name__ == "__main__":
    unittest.main()
