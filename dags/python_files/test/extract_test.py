import boto3
import os
from moto import mock_s3
import sys

# Get the current working directory
directory = os.getcwd()

# Set the path to the folder containing the Python files
python_files_folder = directory + '/../'
sys.path.insert(1, python_files_folder)

import algolia_configuration as configuration
from extract import download_file_from_bucket


@mock_s3
def test_download_file():
    """
    Test case for the download_file_from_bucket function.

    Uses the moto library to mock the S3 service for testing.

    Raises:
        AssertionError: If the downloaded file does not exist.
    """
    # We need to create the bucket since this is all in Moto's 'virtual' AWS account
    s3 = boto3.client('s3', region_name='us-east-1')

    # Import all configuration
    my_bucket = configuration.BUCKET
    s3.create_bucket(Bucket=my_bucket)
    bucket_file = configuration.FILE_NAME
    path = python_files_folder + '/../staging/{file}'.format(file=bucket_file)
    key_id = configuration.AWS_ACCESS_KEY_ID
    secret_key = configuration.AWS_SECRET_ACCESS_KEY

    try:
        os.remove(path)
    except OSError:
        pass

    s3.put_object(Bucket=my_bucket, Key=bucket_file, Body='')

    download_file_from_bucket(bucket_name=my_bucket, file_name=bucket_file, local_path=path,
                              aws_access_key_id=key_id, aws_secret_access_key=secret_key)

    assert os.path.isfile(path)
