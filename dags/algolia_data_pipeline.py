from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
import os
import sys
import csv
from glob import glob
# to get the current working directory
directory = os.getcwd()
# caution: path[0] is reserved for script path (or '' in REPL)
python_files_folder = directory + '/dags/python_files/'
sys.path.insert(1, '/opt/airflow/dags/python_files')

import algolia_configuration as configuration

# Define the DAG
# Explains start_date and end_date
# https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dag-run.html#data-interval
# https://airflow.apache.org/docs/apache-airflow/1.10.13/scheduler.html
# In order to trigger manually in Airflow we need to comment end_date
dag = DAG(
    'algolia_data_pipeline',
    description='A simple data pipeline DAG',
    schedule_interval='0 2 * * *',  # Runs once daily at 2 AM
    start_date=datetime(2019, 3, 31),  # Set start to 2019-03-31 to start running  2019-04-01
 #   end_date=datetime(2019, 4, 8), # Set end to 2019-04-08 to finish run 2019-04-07
    catchup=False
)


def create_test_csv(path_staging):
    """
    Create a test CSV file for staging.

    Args:
        path_staging (str): Path to the staging CSV file.
    """
    header = ['application_id', 'index_prefix']
    values = [
        [1, "shopify_"],
        [2, "shopify"],
        [3, "shopify_"],
        [4, "shopify"],
        [None, "shopify_"],
        [None, "shopify"]
    ]

    with open(path_staging, 'w') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(values)


def extract_function():
    """
    Perform the extract step.

    Calls the download function from the extract module and downloads the file from the S3 bucket.
    """
    import extract

    print("extract imported")

    # Get all variables values from configuration file
    file_name = configuration.FILE_NAME
    bucket_name = configuration.BUCKET
    local_path = configuration.LOCAL_PATH_STAGING.format(file=file_name)
    aws_access_key_id = configuration.AWS_ACCESS_KEY_ID
    aws_secret_access_key = configuration.AWS_SECRET_ACCESS_KEY
    print("All conf loaded")
    if (configuration.IS_TEST):
        create_test_csv(local_path)

    extract.download_file_from_bucket(aws_access_key_id, aws_secret_access_key, bucket_name, file_name, local_path)


# File for the transform step
script_path = python_files_folder + configuration.PYSPARK_FILE_PATH




def load_function():
    """
    Perform the load step.

    Calls the load function from the load module and loads the transformed data into PostgreSQL.
    """
    import load

    host = configuration.HOST
    port = configuration.PORT
    database = configuration.DATABASE
    user = configuration.USER
    password = configuration.PASSWORD
    table_name = configuration.TABLE_NAME
    file_name = configuration.FILE_NAME
    folder_path = configuration.LOCAL_PATH_FINAL.format(file=file_name) + '/*.csv'
    '''
    Pyspark write csv files in a .csv folder known, but the file name is unknown, 
    this allows us to get the file name
    '''
    file_path = glob(folder_path)
    print("All conf loaded")

    load.load_csv_to_postgres(host, port, database, user, password, file_path[0], table_name)


# Define the tasks
download_task = PythonOperator(
    task_id='extract_task',
    python_callable=extract_function,
    dag=dag
)

transform_task = BashOperator(
    task_id='transform_task',
    bash_command='spark-submit --master local[*] ' + script_path,
    dag=dag
)

load_task = PythonOperator(
    task_id='load_task',
    python_callable=load_function,
    dag=dag
)

# Define the task dependencies
download_task >> transform_task >> load_task