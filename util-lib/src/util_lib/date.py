from datetime import datetime
from enum import IntEnum


class Month(IntEnum):
    JANUARY = 1
    FEBRUARY = 2
    MARCH = 3
    APRIL = 4
    MAY = 5
    JUNE = 6
    JULY = 7
    AUGUST = 8
    SEPTEMBER = 9
    OCTOBER = 10
    NOVEMBER = 11
    DECEMBER = 12


def reformat_date(
    input_date: str, source_format: str = "%d-%m-%Y", target_format: str = "%Y-%m-%d"
) -> str:
    """
    Given a string representing a date in a specific format, convert it to a
    different format.
    :param input_date: The string representing a date to convert.
    :param source_format: The format of the string above.
    :param target_format: The format of the desired string.
    :return: A string representation of the input date in the desired format.
    """
    return datetime.strptime(input_date, source_format).strftime(target_format)


def main() -> None:
    print("running.")


if __name__ == "__main__":
    main()
