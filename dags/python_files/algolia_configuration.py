from datetime import date

# Test flag
IS_TEST = True

# AWS connection details
AWS_ACCESS_KEY_ID = "aws_acces_key"
AWS_SECRET_ACCESS_KEY = "aws_acces_secret"
BUCKET = "alg-data-public"

# Database connection details
HOST = 'localhost'
PORT = '5433'
DATABASE = 'algolia_wh'
USER = 'algolia_user'
PASSWORD = 'algolia_pwd'

# Database table name
TABLE_NAME = "postgres_table"

# Files details
today = date.today().strftime("%Y-%m-%d")
FILE_NAME = "test_" + today + ".csv" if IS_TEST else today + ".csv"
LOCAL_PATH_STAGING = "/opt/airflow/dags/staging/{file}"
LOCAL_PATH_FINAL = "/opt/airflow/dags/final/{file}"

# PySpark file path
PYSPARK_FILE_PATH = 'transform.py'
