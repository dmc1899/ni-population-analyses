"""
This module contains unit tests for the file operations in the util_lib.file module.
The tests cover various scenarios such as file existence, file hashing, file download,
file validation against a schema, and file saving logic.
"""

import json
from typing import Dict
from unittest.mock import patch, mock_open, Mock
import pytest

from util_lib.error import InvalidFileError
from util_lib.file import (
    download_new_file,
    get_json_content_from_file,
    validate_json_file_against_schema_file,
    _save_only_if_new,
)


@pytest.fixture
def mock_file_operations() -> None:
    with patch("util_lib.file._is_file_present") as mock_file_exists, patch(
        "util_lib.file.calculate_file_hash"
    ) as mock_calculate_file_hash, patch(
        "util_lib.file._delete_file"
    ) as mock_delete_file, patch(
        "util_lib.file._rename_file"
    ) as mock_rename_file:
        yield mock_file_exists, mock_calculate_file_hash, mock_delete_file, mock_rename_file


def test_save_only_if_new_file_does_not_exist(mock_file_operations, capfd) -> None:
    mock_file_exists, mock_calculate_file_hash, mock_delete_file, mock_rename_file = (
        mock_file_operations
    )
    mock_file_exists.return_value = False

    _save_only_if_new("hash", "algorithm", "temp_path", "to_path")
    mock_rename_file.assert_called_once_with("temp_path", "to_path")


def test_save_only_if_new_file_identical(mock_file_operations: Mock, capfd) -> None:
    mock_file_exists, mock_calculate_file_hash, mock_delete_file, mock_rename_file = (
        mock_file_operations
    )
    mock_file_exists.return_value = True
    mock_calculate_file_hash.return_value = "hash"

    _save_only_if_new("hash", "algorithm", "temp_path", "to_path")

    mock_delete_file.assert_called_once_with("temp_path")
    mock_rename_file.assert_not_called()


@patch("util_lib.file._is_valid_url")
@patch("util_lib.file._create_directory_if_not_exists")
@patch("util_lib.file._save_temp_file")
@patch("util_lib.file._download_file")
@patch("util_lib.file.calculate_file_hash")
@patch("util_lib.file._save_only_if_new")
def test_download_new_file_success_new_file(
    mock_save_only_if_new: Mock,
    mock_calculate_file_hash: Mock,
    mock_download_file: Mock,
    mock_save_temp_file: Mock,
    mock_create_directory_if_not_exists: Mock,
    mock_is_valid_url: Mock,
) -> None:
    mock_is_valid_url.return_value = True
    mock_download_file.return_value = b"file_content"
    mock_calculate_file_hash.return_value = "hash"
    mock_save_only_if_new.return_value = None

    download_new_file("http://example.com/file.txt", "/path/to/file.txt")

    mock_create_directory_if_not_exists.assert_called_once_with("/path/to/file.txt")
    mock_save_temp_file.assert_called_once_with(
        "/path/to/file.txt.tmp", b"file_content"
    )
    mock_calculate_file_hash.assert_called_once_with("/path/to/file.txt.tmp", "sha256")
    mock_save_only_if_new.assert_called_once_with(
        "hash", "sha256", "/path/to/file.txt.tmp", "/path/to/file.txt"
    )


@patch("util_lib.file._is_valid_url")
@patch("util_lib.file._create_directory_if_not_exists")
@patch("util_lib.file._save_temp_file")
@patch("util_lib.file._download_file")
@patch("util_lib.file.calculate_file_hash")
@patch("util_lib.file._save_only_if_new")
@patch("util_lib.file._is_file_present")
def test_download_new_file_success_existing_file(
    mock_file_exists: Mock,
    mock_save_only_if_new: Mock,
    mock_calculate_file_hash: Mock,
    mock_download_file: Mock,
    mock_save_temp_file: Mock,
    mock_create_directory_if_not_exists: Mock,
    mock_is_valid_url: Mock,
) -> None:
    mock_is_valid_url.return_value = True
    mock_download_file.return_value = b"file_content"
    mock_calculate_file_hash.return_value = "hash"
    mock_save_only_if_new.return_value = None
    mock_file_exists.return_value = True

    download_new_file("http://example.com/file.txt", "/path/to/file.txt")

    mock_create_directory_if_not_exists.assert_called_once_with("/path/to/file.txt")
    mock_save_temp_file.assert_called_once_with(
        "/path/to/file.txt.tmp", b"file_content"
    )
    mock_calculate_file_hash.assert_called_once_with("/path/to/file.txt.tmp", "sha256")
    mock_save_only_if_new.assert_called_once_with(
        "hash", "sha256", "/path/to/file.txt.tmp", "/path/to/file.txt"
    )


def test_download_new_file_invalid_url() -> None:
    with patch("util_lib.file._is_valid_url") as mock_is_valid_url:
        mock_is_valid_url.return_value = False

        with pytest.raises(InvalidFileError) as exc_info:
            download_new_file("invalid_url", "to_path")

        assert (
            str(exc_info.value)
            == "Invalid URL. The URL should start with 'http://' or 'https://'."
        )


@patch("builtins.open", new_callable=mock_open, read_data='{"key": "value"}')
def test_valid_json_yet_again(mock_file: Mock) -> None:
    expected_output = {"key": "value"}
    result = get_json_content_from_file("dummy_file.json")
    assert result == expected_output


@patch("builtins.open", new_callable=mock_open, read_data="{}")
def test_empty_json(mock_file: Mock) -> None:
    expected_output = {}
    result = get_json_content_from_file("dummy_file.json")
    assert result == expected_output


@patch("builtins.open", new_callable=mock_open, read_data="{invalid json}")
def test_invalid_json_again(mock_file: Mock) -> None:
    with pytest.raises(json.JSONDecodeError):
        get_json_content_from_file("dummy_file.json")


@patch("builtins.open", side_effect=FileNotFoundError)
def test_non_existent_file(mock_file: Mock) -> None:
    with pytest.raises(FileNotFoundError):
        get_json_content_from_file("dummy_file.json")


def mock_get_json_content_from_file_raises_jsondecodeerror(file: str) -> None:
    raise json.JSONDecodeError("Expecting value", file, 0)


@patch(
    "util_lib.file.get_json_content_from_file",
    side_effect=mock_get_json_content_from_file_raises_jsondecodeerror,
)
def test_json_decode_error(mock_get_json: Mock) -> None:
    with pytest.raises(json.JSONDecodeError):
        validate_json_file_against_schema_file("dummy_file.json", "dummy_schema.json")


valid_json_content = {"name": "John", "age": 30}
valid_json_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "age": {"type": "number"},
    },
    "required": ["name", "age"],
}

invalid_json_content = {"name": "John", "age": "thirty"}  # age should be a number
invalid_json_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "age": {"type": "string"},
    },
    "required": ["name", "age"],
}


def mock_get_json_content_from_file(file: str) -> Dict:
    if file == "valid_json_file":
        return valid_json_content
    if file == "valid_schema_file":
        return valid_json_schema
    if file == "invalid_json_file":
        return invalid_json_content
    if file == "invalid_schema_file":
        return invalid_json_schema
    return {}


@patch(
    "util_lib.file.get_json_content_from_file",
    side_effect=mock_get_json_content_from_file,
)
def test_valid_json(mock_get_json: Mock) -> None:
    result, message = validate_json_file_against_schema_file(
        "valid_json_file", "valid_schema_file"
    )
    assert result is True
    assert message == "JSON document is valid."


@patch(
    "util_lib.file.get_json_content_from_file",
    side_effect=mock_get_json_content_from_file,
)
def test_invalid_json(mock_item: Mock) -> None:
    result, _ = validate_json_file_against_schema_file(
        "invalid_json_file", "valid_schema_file"
    )
    assert result is False


@patch(
    "util_lib.file.get_json_content_from_file",
    side_effect=mock_get_json_content_from_file,
)
def test_invalid_schema(mock_item: Mock) -> None:
    result, _ = validate_json_file_against_schema_file(
        "valid_json_file", "invalid_schema_file"
    )
    assert result is False

