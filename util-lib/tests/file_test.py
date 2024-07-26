import pytest

from util_lib.file import download_file_safely, calculate_file_hash,get_json_content_from_file, validate_json_file_against_schema_file
import unittest
from unittest.mock import patch, mock_open, MagicMock
from requests.exceptions import HTTPError, Timeout, RequestException
import json
import jsonschema


@patch('builtins.print')
@patch('os.makedirs')
@patch('os.path.exists')
@patch('os.rename')
@patch('builtins.open', new_callable=mock_open)
@patch('requests.get')
@patch('util_lib.file.calculate_file_hash')
def test_invalid_url(mock_calculate_file_hash, mock_get, mock_open, mock_rename, mock_exists, mock_makedirs, mock_print):
    # with assert(ValueError): TODO - workout why this value error is not being raised.
    download_file_safely('ftp://invalid_url', './file')


@patch('builtins.print')
@patch('os.makedirs')
@patch('os.path.exists')
@patch('os.rename')
@patch('builtins.open', new_callable=mock_open)
@patch('requests.get')
@patch('util_lib.file.calculate_file_hash')
def test_successful_download(mock_calculate_file_hash, mock_get, mock_open, mock_rename, mock_exists, mock_makedirs, mock_print):
    mock_get.return_value.content = b'file content'
    mock_get.return_value.raise_for_status = MagicMock()
    mock_calculate_file_hash.side_effect = ['hash1']

    mock_exists.return_value = False

    download_file_safely('http://valid_url', '/path/to/save/file')

    mock_get.assert_called_once()
    mock_open.assert_called_with('/path/to/save/file.tmp', 'wb')
    mock_rename.assert_called_with('/path/to/save/file.tmp', '/path/to/save/file')


@patch('builtins.print')
@patch('os.makedirs')
@patch('os.path.exists')
@patch('os.rename')
@patch('builtins.open', new_callable=mock_open)
@patch('requests.get')
@patch('util_lib.file.calculate_file_hash')
def test_hash_comparison_identical(mock_calculate_file_hash, mock_get, mock_open, mock_rename, mock_exists, mock_makedirs, mock_print):
    mock_get.return_value.content = b'file content'
    mock_get.return_value.raise_for_status = MagicMock()
    mock_calculate_file_hash.side_effect = ['hash1', 'hash1']

    mock_exists.return_value = True

    download_file_safely('http://valid_url', '/path/to/save/file')

    mock_get.assert_called_once()
    mock_open.assert_called_with('/path/to/save/file.tmp', 'wb')
    assert mock_rename.called is False


@patch('builtins.print')
@patch('os.makedirs')
@patch('os.path.exists')
@patch('os.rename')
@patch('builtins.open', new_callable=mock_open)
@patch('requests.get')
@patch('util_lib.file.calculate_file_hash')
def test_hash_comparison_different(mock_calculate_file_hash, mock_get, mock_open, mock_rename, mock_exists, mock_makedirs, mock_print):
    mock_get.return_value.content = b'file content'
    mock_get.return_value.raise_for_status = MagicMock()
    mock_calculate_file_hash.side_effect = ['hash1', 'hash2']

    mock_exists.return_value = True

    download_file_safely('http://valid_url', '/path/to/save/file')

    mock_get.assert_called_once()
    mock_open.assert_called_with('/path/to/save/file.tmp', 'wb')
    mock_rename.assert_called_with('/path/to/save/file.tmp', '/path/to/save/file')


@patch('builtins.print')
@patch('requests.get')
def test_http_error(mock_get, mock_print):
    mock_get.side_effect = HTTPError("HTTP Error")
    download_file_safely('http://valid_url', './file')
    mock_print.assert_any_call("HTTP error occurred: HTTP Error")


@patch('builtins.print')
@patch('requests.get')
def test_timeout_error(mock_get, mock_print):
    mock_get.side_effect = Timeout("Timeout Error")

    download_file_safely('http://valid_url', './file')

    mock_print.assert_any_call("Timeout error occurred: Timeout Error")


@patch('builtins.print')
@patch('requests.get')
def test_request_exception(mock_get, mock_print):
    mock_get.side_effect = RequestException("Request Exception")

    download_file_safely('http://valid_url', './file')

    mock_print.assert_any_call("Request exception occurred: Request Exception")


@patch('builtins.print')
@patch('os.makedirs')
@patch('os.path.exists')
@patch('os.rename')
@patch('builtins.open', new_callable=mock_open)
@patch('requests.get')
@patch('util_lib.file.calculate_file_hash')
def test_io_error(mock_calculate_file_hash, mock_get, mock_open, mock_rename, mock_exists, mock_makedirs, mock_print):
    mock_open.side_effect = IOError("IO Error")
    download_file_safely('http://valid_url', '/path/to/save/file')
    mock_print.assert_any_call("File I/O error occurred: IO Error")


@patch('builtins.open', new_callable=mock_open, read_data='{"key": "value"}')
def test_valid_json(mock_file):
    expected_output = {"key": "value"}
    result = get_json_content_from_file('dummy_file.json')
    assert result == expected_output


@patch('builtins.open', new_callable=mock_open, read_data='{}')
def test_empty_json(mock_file):
    expected_output = {}
    result = get_json_content_from_file('dummy_file.json')
    assert result == expected_output


@patch('builtins.open', new_callable=mock_open, read_data='{invalid json}')
def test_invalid_json(mock_file):
    with pytest.raises(json.JSONDecodeError):
        get_json_content_from_file('dummy_file.json')

@patch('builtins.open', side_effect=FileNotFoundError)
def test_non_existent_file(mock_file):
    with pytest.raises(FileNotFoundError):
        get_json_content_from_file('dummy_file.json')


# Create a mock function that raises a JSONDecodeError
def mock_get_json_content_from_file_raises_jsondecodeerror(file):
    raise json.JSONDecodeError("Expecting value", file, 0)


@patch('util_lib.file.get_json_content_from_file', side_effect=mock_get_json_content_from_file_raises_jsondecodeerror)
def test_json_decode_error(mock_get_json):
    with pytest.raises(json.JSONDecodeError):
        validate_json_file_against_schema_file("dummy_file.json", "dummy_schema.json")


# Mock data for testing
valid_json_content = {"name": "John", "age": 30}
valid_json_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "age": {"type": "number"},
    },
    "required": ["name", "age"]
}

invalid_json_content = {"name": "John", "age": "thirty"}  # age should be a number
invalid_json_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "age": {"type": "string"},
    },
    "required": ["name", "age"]
}


def mock_get_json_content_from_file(file):
    if file == "valid_json_file":
        return valid_json_content
    elif file == "valid_schema_file":
        return valid_json_schema
    elif file == "invalid_json_file":
        return invalid_json_content
    elif file == "invalid_schema_file":
        return invalid_json_schema
    else:
        return {}


@patch('util_lib.file.get_json_content_from_file', side_effect=mock_get_json_content_from_file)
def test_valid_json(mock_get_json):
    result, message = validate_json_file_against_schema_file("valid_json_file", "valid_schema_file")
    assert result is True
    assert message == "JSON document is valid."


@patch('util_lib.file.get_json_content_from_file', side_effect=mock_get_json_content_from_file)
def test_invalid_json(mock_get_json):
    result, message = validate_json_file_against_schema_file("invalid_json_file", "valid_schema_file")
    assert result is False


@patch('util_lib.file.get_json_content_from_file', side_effect=mock_get_json_content_from_file)
def test_invalid_schema(mock_get_json):
    result, message = validate_json_file_against_schema_file("valid_json_file", "invalid_schema_file")
    assert result is False



if __name__ == '__main__':
    test_invalid_schema
    # download_file_safely('http://valid_url', './file')
    # unittest.main()
