import os
import requests
from requests.exceptions import RequestException, HTTPError, Timeout
from hashlib import sha256

LOCAL_CA_CERTIFICATE_FILE_PATH = "/path/to/ca/certificate.pem"

def calculate_file_hash(file_path, hash_algorithm='sha256'):
    """
    Calculate the hash of a file using the specified hash algorithm.

    :param file_path: Path to the file.
    :param hash_algorithm: Hash algorithm to use (default is 'sha256').
    :return: The calculated hash of the file.
    """
    hash_func = getattr(hashlib, hash_algorithm)()
    with open(file_path, 'rb') as file:
        while True:
            data = file.read(65536)  # Read in chunks of 64KB
            if not data:
                break
            hash_func.update(data)
    return hash_func.hexdigest()

def download_file_safely(from_path, to_path, hash_algorithm='sha256'):
    """
    Downloads a file from the specified URL to the local path with error handling and hash comparison.

    :param from_path: URL of the file to download.
    :param to_path: Local path where the file will be saved.
    :param hash_algorithm: Hash algorithm to use for comparing files (default is 'sha256').
    """
    try:
        # Check if the URL is valid
        if not from_path.startswith(('http://', 'https://')):
            raise ValueError("Invalid URL. The URL should start with 'http://' or 'https://'.")

        # Check if the directory for to_path exists
        os.makedirs(os.path.dirname(to_path), exist_ok=True)

        # Make the request to download the file
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
        raise ve
    except HTTPError as http_err:
        raise http_err
    except Timeout as timeout_err:
        raise timeout_err
    except RequestException as req_err:
        raise req_err
    except IOError as io_err:
        raise io_err
    except Exception as err:
        raise err
