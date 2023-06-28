from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when
import algolia_configuration as configuration


def transform_df(df):
    """
    Transforms a DataFrame by filtering rows and adding a new column.

    Args:
        df (pyspark.sql.DataFrame): The input DataFrame.

    Returns:
        pyspark.sql.DataFrame: The transformed DataFrame.
    """
    # Filter the DataFrame based on the application_id column
    filtered_df = df.filter(col("application_id").isNotNull())

    # Add a new column named has_specific_prefix
    df_final = filtered_df.withColumn("has_specific_prefix", when(col("index_prefix").startswith("shopify_"), True).otherwise(False))

    return df_final


def main():
    """
    Main entry point for the transformation process.
    """
    # Create a SparkSession
    spark = SparkSession.builder.appName("CSV_Filter_Add_Column").getOrCreate()

    # Read the CSV file into a DataFrame
    file_read = configuration.LOCAL_PATH_STAGING.format(file=configuration.FILE_NAME)
    df = spark.read.csv(file_read, header=True, inferSchema=True)

    # Transform the DataFrame
    df_final = transform_df(df)

    # Save the DataFrame as a new CSV file
    file_write = configuration.LOCAL_PATH_FINAL.format(file=configuration.FILE_NAME)
    df_final.write.csv(file_write, header=False, mode="overwrite")

    # Stop the SparkSession
    spark.stop()


if __name__ == "__main__":
    main()
