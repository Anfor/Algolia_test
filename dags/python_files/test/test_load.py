import pytest
from unittest.mock import Mock, call, patch
import os
import sys

# Get the current working directory
directory = os.getcwd()

# Set the path to the folder containing the Python files
python_files_folder = directory + '/../'
sys.path.insert(1, python_files_folder)
from load import load_csv_to_postgres


@pytest.mark.parametrize(
    "host, port, database, user, password, file_name, table_name",
    [("localhost", 5432, "postgres", "postgres", "password", "./test_data.csv", "test_table")]
)


def test_load_csv_to_postgres(host, port, database, user, password, file_name, table_name):
    """
    Test case for the load_csv_to_postgres function.

    Uses the unittest.mock.patch decorator to mock the psycopg2.connect and psycopg2.connect.cursor methods.

    Args:
        host (str): The host of the PostgreSQL database.
        port (int): The port number of the PostgreSQL database.
        database (str): The name of the PostgreSQL database.
        user (str): The username for the PostgreSQL database.
        password (str): The password for the PostgreSQL database.
        file_name (str): The path to the CSV file to be loaded.
        table_name (str): The name of the table in the PostgreSQL database.
    """
    with patch("psycopg2.connect") as mock_connect:
        # Create mock objects for the connection and cursor
        mock_connection = mock_connect.return_value
        mock_cursor = mock_connection.cursor.return_value

        # Call the function to load CSV data into PostgreSQL
        load_csv_to_postgres(host, port, database, user, password, file_name, table_name)

        # Assertions
        mock_connect.assert_called_once_with(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password
        )

        # Define the expected calls to mock_cursor.execute
        calls = [
            call(
                'CREATE TABLE IF NOT EXISTS test_table (application_id INTEGER, index_prefix TEXT, has_specific_prefix BOOLEAN)'),
            call('INSERT INTO test_table VALUES (%s, %s, %s)', (1, 'shopify_', True)),
            call('INSERT INTO test_table VALUES (%s, %s, %s)', (2, 'shopify', False)),
            call('INSERT INTO test_table VALUES (%s, %s, %s)', (3, 'shopify_', True)),
            call('INSERT INTO test_table VALUES (%s, %s, %s)', (4, 'shopify', False))
                 ]

        mock_connection.cursor.assert_called_once()
        mock_cursor.execute.assert_has_calls(calls, any_order=True)
