"""
 Custom exceptions.
"""


class InvalidFileError(Exception):
    """
    Exception raised when a file is invalid.
    """

    def __init__(self, message:str) -> None:
        super().__init__(message)
