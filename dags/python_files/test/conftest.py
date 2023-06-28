"""Pytest fixtures that can be reused across tests. The filename needs to be conftest.py."""
import findspark  # This needs to be the first import
findspark.init()

import logging
import pytest
from pyspark.sql import SparkSession


def quiet_py4j():
    """Turn down Spark logging for the test context."""
    logger = logging.getLogger('py4j')
    logger.setLevel(logging.WARN)


@pytest.fixture(scope="session")
def spark_session(request):
    """
    Pytest fixture for creating a SparkSession.

    Args:
        request: pytest request object.

    Returns:
        pyspark.sql.SparkSession: The SparkSession object.

    Finalizer:
        Stops the SparkSession and SparkContext at the end of the test session.
    """
    spark_session = SparkSession.builder \
        .master("local[*]") \
        .appName("some-app-name") \
        .getOrCreate()

    request.addfinalizer(lambda: spark_session.sparkContext.stop())

    return spark_session
