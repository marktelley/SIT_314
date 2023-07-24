# README

## Project Description

This Python script collects cycling power service data from a Bluetooth Low Energy (BLE) device using the bleak library, stores it in a Pandas DataFrame, then exports the data to a CSV file and uploads it to a Google BigQuery table.

## Dependencies

This script requires the following Python libraries:

- asyncio: Provides infrastructure for writing single-threaded concurrent code using coroutines, multiplexing I/O access over sockets and other resources.
- bleak: A GATT client software, capable of connecting to BLE devices acting as GATT servers. It is used for communicating with the device.
- pandas: A powerful data analysis and manipulation library.
- google-cloud-bigquery: A Python client library for Google BigQuery, used to make requests to BigQuery from the script.
- pyarrow: A Python library that provides C++ implementations for manipulating and interfacing with Arrow-based data, often used with pandas for efficient I/O operations with Parquet files and with BigQuery.

Furthermore, the script imports a custom module named `cycling_power_service`, which needs to be present in the same directory as this script - You can find more infomation about this script via [PyCycling](https://pypi.org/project/pycycling/).

## Usage

To use this script:

1. Replace the `device_address` variable with your BLE device's address. You can use the `discover.py` script to retrieve your device's address.

2. Adjust the `session_length` variable to set the desired duration for the data collection session in seconds.

3. Note the requirements below for Google BigQuery / Console set up. 

4. Run the script in your Python environment. 

The script will attempt to connect to the specified BLE device, collect the cycling power data, and store it in a pandas DataFrame. Once the data collection session is over, the DataFrame is written to a CSV file named "Activity_Data.csv".

Next, the script attempts to connect to a Google BigQuery service using a service account JSON file and uploads the data to a specified BigQuery table.

## Google BigQuery Setup

Before running the script, make sure you have set up the Google Cloud SDK and authenticated your service account. Provide the path to the service account JSON file in the `bigquery.Client.from_service_account_json()` method.

Also, specify your Google BigQuery dataset and table in the `table_id` variable in the format "dataset.table". The script attempts to create this table if it does not already exist.

## Output

The script prints the collected data in the console and writes it to a CSV file named "Activity_Data.csv". It also uploads the data to a Google BigQuery table.

## Debugging

The script sets the PYTHONASYNCIODEBUG environment variable to 1 to print more detailed debugging information from asyncio.

## Visualisation

To see the data visualisation (cadence and power only), access the Google Looker Studio Dashboard (link below). The dashboard is connected to the BigQuery table where the data is uploaded.

[Google Looker Studio Dashboard](https://lookerstudio.google.com/reporting/XXXXXXXXX)
