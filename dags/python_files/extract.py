import boto3


def download_file_from_bucket(bucket_name, file_name, local_path, aws_access_key_id, aws_secret_access_key):
    """
    Downloads a file from an S3 bucket.

    Args:
        bucket_name (str): The name of the S3 bucket.
        file_name (str): The name of the file in the S3 bucket.
        local_path (str): The local path where the file will be downloaded to.
        aws_access_key_id (str): The AWS access key ID.
        aws_secret_access_key (str): The AWS secret access key.

    Raises:
        Exception: If an error occurs while downloading the file.
    """
    # Create an instance of the S3 client
    s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

    try:
        # Download the file from the bucket
        s3.download_file(bucket_name, file_name, local_path)
        print("File downloaded successfully.")
    except Exception as e:
        print("Error downloading the file: ", e)
