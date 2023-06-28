import psycopg2
import csv


def load_csv_to_postgres(host, port, database, user, password, file_path, table_name, header=False):
    print("File_path CSV file: ")
    print(file_path)

    """
    Loads data from a CSV file into a PostgreSQL table.

    Args:
        host (str): The host of the PostgreSQL database.
        port (str): The port number of the PostgreSQL database.
        database (str): The name of the PostgreSQL database.
        user (str): The username for the PostgreSQL database.
        password (str): The password for the PostgreSQL database.
        file_path (str): The path to the CSV file to be loaded.
        table_name (str): The name of the table in the PostgreSQL database.
        header (bool, optional): Specifies if the CSV file has a header row. Defaults to False.

    Raises:
        psycopg2.Error: If an error occurs while loading data to PostgreSQL.
    """


    # Establish a connection to the PostgreSQL database
    conn = psycopg2.connect(
        host=host,
        port=port,
        database=database,
        user=user,
        password=password
    )
    cursor = conn.cursor()

    try:
        # Create the table in the database
        create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} (application_id INTEGER, index_prefix TEXT, has_specific_prefix BOOLEAN)"
        cursor.execute(create_table_query)
        conn.commit()
        print("Table created successfully.")

        # Load data from the CSV file into the table
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            if header:
                next(reader)  # Skip the header row if needed
            for row in reader:
                # Convert the columns to the appropriate types
                application_id = int(row[0])
                index_prefix = row[1]
                has_specific_prefix = row[2].lower() == 'true'

                insert_query = f"INSERT INTO {table_name} VALUES (%s, %s, %s)"
                cursor.execute(insert_query, (application_id, index_prefix, has_specific_prefix))
            conn.commit()
        print("Data loaded successfully.")

    except (Exception, psycopg2.Error) as error:
        print("Error loading data to PostgreSQL: ", error)
        raise error

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
        print("Connection to PostgreSQL closed.")
