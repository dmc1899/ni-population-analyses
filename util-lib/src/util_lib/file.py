"""
 Convenience functions for file manipulation and validation.
"""

import os
from typing import Any
import hashlib
import json
import jsonschema
import requests
from typing_extensions import Buffer
from jsonschema import validate

from util_lib.error import InvalidFileError
import logging

logger = logging.getLogger(__name__)

LOCAL_CA_CERTIFICATE_FILE_PATH = (
    "/Users/darraghmcconville/Library/"
    "Caches/pypoetry/virtualenvs/"
    "util-lib-GqhJd4fQ-py3.10/lib/python3.10/"
    "site-packages/certifi/cacert.pem"
)


def download_file(
    from_path: str, to_path: str, ca_cert_path: str = LOCAL_CA_CERTIFICATE_FILE_PATH
) -> None:
    logger.info("downloaded from: " + from_path)

    response = requests.get(from_path, verify=ca_cert_path, timeout=300)

    with open(to_path, "wb") as file:
        file.write(response.content)


def calculate_file_hash(file_path: str, hash_algorithm: str = "sha256") -> str:
    """
    Calculate the hash of a file using the specified hash algorithm.

    :param file_path: Path to the file.
    :param hash_algorithm: Hash algorithm to use (default is 'sha256').
    :return: Hexadecimal hash string.
    """
    hash_func = hashlib.new(hash_algorithm)
    with open(file_path, "rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            hash_func.update(chunk)
    return hash_func.hexdigest()


def _is_valid_url(url: str) -> bool:
    return url.startswith(("http://", "https://"))


def _create_directory_if_not_exists(path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)


def _download_file(
    from_path: str, ca_cert_path: str = LOCAL_CA_CERTIFICATE_FILE_PATH
) -> bytes:
    response = requests.get(from_path, verify=ca_cert_path, timeout=10)
    response.raise_for_status()
    return response.content


def _save_temp_file(temp_file_path: str, content: Buffer) -> None:
    with open(temp_file_path, "wb") as file:
        file.write(content)


def _calculate_file_hash(file_path: str, algorithm: str = "sha256") -> str:
    hash_func = (
        hashlib.sha256() if algorithm == "sha256" else None
    )
    if hash_func is None:
        raise ValueError(f"Unsupported hash algorithm: {algorithm}")

    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_func.update(chunk)
    return hash_func.hexdigest()


def _is_file_present(path: str) -> bool:
    return os.path.exists(path)


def _delete_file(path: str) -> None:
    os.remove(path)


def _rename_file(src: str, dst: str) -> None:
    os.rename(src, dst)


def _save_only_if_new(
    downloaded_file_hash: str, hash_algorithm: str, temp_file_path: str, to_path: str
) -> None:
    if _is_file_present(to_path):
        existing_file_hash = calculate_file_hash(to_path, hash_algorithm)
        logger.info(f"Hash of existing file: {existing_file_hash}")

        if downloaded_file_hash == existing_file_hash:
            _delete_file(temp_file_path)
        else:
            logger.info(
                "The downloaded file is different from the existing file. The file will be saved."
            )
            _rename_file(temp_file_path, to_path)
    else:
        logger.info("The target file does not exist. The file will be saved.")
        _rename_file(temp_file_path, to_path)


def download_new_file(
    from_path: str, to_path: str, hash_algorithm: str = "sha256"
) -> None:
    if not _is_valid_url(from_path):
        raise InvalidFileError(
            "Invalid URL. The URL should start with 'http://' or 'https://'."
        )

    _create_directory_if_not_exists(to_path)

    temp_file_path = to_path + ".tmp"
    _save_temp_file(temp_file_path, _download_file(from_path))

    downloaded_file_hash = calculate_file_hash(temp_file_path, hash_algorithm)

    _save_only_if_new(downloaded_file_hash, hash_algorithm, temp_file_path, to_path)


def get_json_content_from_file(input_file: str) -> Any:
    with open(input_file, "r", encoding="UTF-8") as file:
        json_content = json.load(file)
    return json_content


def validate_json_file_against_schema_file(
    json_data_file: str, json_schema_file: str
) -> tuple[bool, str]:

    json_content = get_json_content_from_file(json_data_file)
    json_schema = get_json_content_from_file(json_schema_file)

    try:
        validate(instance=json_content, schema=json_schema)
    except jsonschema.exceptions.ValidationError:
        err = "JSON document is invalid and does not conform to the schema."
        return False, err

    message = "JSON document is valid."
    return True, message


if __name__ == "__main__":
    logger.info("main")
