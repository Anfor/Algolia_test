import pytest
import os
import sys

# Get the current working directory
directory = os.getcwd()

# Set the path to the folder containing the Python files
python_files_folder = directory + '/../'
sys.path.insert(1, python_files_folder)
from transform import transform_df

# This allows using the fixture in all tests in this module
pytestmark = pytest.mark.usefixtures("spark_session")


def test_csv_filter_add_column(spark_session):
    """
    Test the transform_df function by filtering and adding a new column to a DataFrame.

    Args:
        spark_session: Test fixture SparkSession.
    """

    # Define the test input data
    test_input = [
        (1, "shopify_"),
        (2, "shopify"),
        (3, "shopify_"),
        (4, "shopify")
    ]

    # Define the columns for the DataFrame
    df_columns = ["application_id", "index_prefix"]

    # Create the test input DataFrame
    df = spark_session.createDataFrame(data=test_input, schema=df_columns)

    # Apply the transform_df function to the DataFrame
    results = transform_df(df)
    results.show()

    # Define the expected test result
    test_input_result = [
        (1, "shopify_", True),
        (2, "shopify", False),
        (3, "shopify_", True),
        (4, "shopify", False)
    ]
    df_columns_result = ["application_id", "index_prefix", "has_specific_prefix"]

    # Create the expected test result DataFrame
    df_result = spark_session.createDataFrame(data=test_input_result, schema=df_columns_result)
    df_result.show()

    # Compare the actual and expected results
    assert sorted(results.collect()) == sorted(df_result.collect())
