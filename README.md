# Algolia_test

Welcome to the Algolia_test project! This project showcases the implementation of Algolia search functionality in a web application.

## Table of Contents
- [Project Overview](#project-overview)
- [Installation](#installation)
- [Usage](#usage)
- [Testing](#testing)

## Project Overview
The Algolia_test project provides a demonstration of integrating Algolia search into a web application. It leverages the Algolia API to provide fast and efficient search capabilities on a specific dataset.

The main objectives of this project are:
- To demonstrate how to set up and configure Algolia for search functionality.
- To answer the test for data engineer.
## Installation
Follow these steps to install and set up the Algolia_test project:

1. Clone the repository:
   ```bash
   git clone git@github.com:Anfor/Algolia_test.git

2. Change to the project directory:

	```bash
   cd Algolia_test

3. Start the project using Docker Compose:

	```bash
	docker-compose up

4. Access the Airflow web UI in your browser at `http://localhost:8080`.
- Use the following credentials to log in:
  - User: airflow
  - Password: airflow

5. Unpause the DAG named `algolia_data_pipeline` in the Airflow web UI.
  -Hints: 
	- In order to trigger manually in Airflow we need to comment end_date in the file `.../algolia_test/dags/algolia_data_pipeline.py`
	- If we run in test mode, confirm the variable `IS_TEST = True` in the file `.../algolia_test/dags/python_files/algolia_configuration.py`

## Usage
Once the Algolia_test project is installed and running, you can use it as follows:

1. Configure the necessary variables in the `python_files/algolia_configuration.py` file.
- Update the variables according to your specific setup and requirements.

2. Run the data pipeline:
- If you want to trigger the pipeline manually in Airflow, comment out the `end_date` parameter in the `algolia_data_pipeline.py` file.
- If running in test mode, ensure that the variable `IS_TEST` in the `python_files/algolia_configuration.py` file is set to `True`.
- If running in production mode, set `IS_TEST` to `False` and execute the pipeline.

3. Monitor the execution of the data pipeline in the Airflow web UI.

## Testing
To run tests in the Algolia_test project, follow these steps:

1. Open a terminal.

2. Run the following command to list the running Docker containers and identify the `container_id` for the `airflow_webserver` container:
	```bash
	docker ps

3. Run the following command to enter the Docker container's terminal:
	```bash
	docker exec -it <container_id> bash

4. Change to the `dags/python_files/test/` directory:
	```bash
	cd dags/python_files/test/

5. Run the following command to test the extraction from S3:
	```bash
	pytest extract_test.py

6. Run the following command to test the transformation step in PySpark:
	```bash
	pytest test_transform.py

7. Run the following command to test the PostgreSQL load step using data from the `.../test_data.csv` file:
	```bash
	pytest test_load.py

## Hints:

In `.../dags/final/test_[YYYY-MM-DD].csv/*.csv` you can see the result of running transform step, 
the source before pyspark transformation   comes from the folder 
`.../dags/staging/test_[YYYY-MM-DD].csv` that is produced in the `create_test_csv` 
function in file `.../algolia_test/dags/algolia_data_pipeline.py`
The prefix `test_` is added just in case that runs in test mode.

