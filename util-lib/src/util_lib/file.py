import requests
from requests.exceptions import HTTPError, Timeout, RequestException
import os
import hashlib
import json
import jsonschema
from jsonschema import validate
import requests

from util_lib.errors import InvalidFileError

LOCAL_CA_CERTIFICATE_FILE_PATH='/Users/darraghmcconville/Library/Caches/pypoetry/virtualenvs/util-lib-GqhJd4fQ-py3.10/lib/python3.10/site-packages/certifi/cacert.pem'


def download_file(from_path, to_path):
    print("downloaded from: " + from_path)

    response = requests.get(from_path, verify=LOCAL_CA_CERTIFICATE_FILE_PATH)

    with open(to_path, 'wb') as file:
        file.write(response.content)


def calculate_file_hash(file_path, hash_algorithm='sha256'):
    """
    Calculate the hash of a file using the specified hash algorithm.

    :param file_path: Path to the file.
    :param hash_algorithm: Hash algorithm to use (default is 'sha256').
    :return: Hexadecimal hash string.
    """
    hash_func = hashlib.new(hash_algorithm)
    with open(file_path, 'rb') as file:
        for chunk in iter(lambda: file.read(4096), b""):
            hash_func.update(chunk)
    return hash_func.hexdigest()


def download_file_safely(from_path, to_path, hash_algorithm='sha256'):
    """
    Downloads a file from the specified URL to the local path with error handling and hash comparison.

    :param from_path: URL of the file to download.
    :param to_path: Local path where the file will be saved.
    :param hash_algorithm: Hash algorithm to use for comparing files (default is 'sha256').
    """
    try:
        if not from_path.startswith(('http://', 'https://')):
            print("Invalid URL. The URL should start with 'http://' or 'https://'.")
            raise InvalidFileError("Invalid URL. The URL should start with 'http://' or 'https://'.")

        os.makedirs(os.path.dirname(to_path), exist_ok=True)

        print(f"Starting download from: {from_path}")
        response = requests.get(from_path, verify=LOCAL_CA_CERTIFICATE_FILE_PATH, timeout=10)

        # Raise an HTTPError for bad responses (4xx and 5xx)
        response.raise_for_status()

        # Create a temporary file path
        temp_file_path = to_path + '.tmp'

        # Write the content to a temporary file path
        with open(temp_file_path, 'wb') as file:
            file.write(response.content)

        print(f"Downloaded to temporary path: {temp_file_path}")

        # Calculate hash of the downloaded file
        downloaded_file_hash = calculate_file_hash(temp_file_path, hash_algorithm)
        print(f"Hash of downloaded file: {downloaded_file_hash}")

        # Check if the target file already exists
        if os.path.exists(to_path):
            existing_file_hash = calculate_file_hash(to_path, hash_algorithm)
            print(f"Hash of existing file: {existing_file_hash}")

            if downloaded_file_hash == existing_file_hash:
                print("The downloaded file is identical to the existing file. The file will not be saved.")
                os.remove(temp_file_path)
                return
            else:
                print("The downloaded file is different from the existing file. The file will be saved.")
        else:
            print("The target file does not exist. The file will be saved.")

        # Save the downloaded file to the target path
        os.rename(temp_file_path, to_path)
        print(f"File saved to: {to_path}")

    except ValueError as ve:
        print(f"ValueError: {ve}")
    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Timeout as timeout_err:
        print(f"Timeout error occurred: {timeout_err}")
    except RequestException as req_err:
        print(f"Request exception occurred: {req_err}")
    except IOError as io_err:
        print(f"File I/O error occurred: {io_err}")
    except Exception as err:
        print(f"An unexpected error occurred: {err}")


def get_json_content_from_file(file):
    with open(file, 'r') as file:
        json_content = json.load(file)
    return json_content


def validate_json_file_against_schema_file(json_data_file, json_schema_file) -> tuple[bool, str]:

    json_content = get_json_content_from_file(json_data_file)
    json_schema = get_json_content_from_file(json_schema_file)

    try:
        validate(instance=json_content, schema=json_schema)
    except jsonschema.exceptions.ValidationError as err:
        err = "JSON document is invalid and does not conform to the schema."
        return False, err

    message = "JSON document is valid."
    return True, message


if __name__ == '__main__':
    valid_json_content = {"name": "John", "age": 30}
    invalid_json_schema = {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "age": {"type": "string"},
        },
        "required": ["name", "age"]
    }
    validate_json_file_against_schema_file("valid_json_content.json", "invalid_json_schema.json")
    print('fat')
    #download_file_safely('ftp://invalid_url', './file')
    #download_file_safely('\https://www.nisra.gov.uk/system/files/statistics/Weekly_Deaths%20-%20w%20e%2017%20May%202024.xlsx', './files/file.txt')