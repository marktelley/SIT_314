# Sensor Data Retrieval and Storage

## Overview

This script collects data from a wireless sensor with tag_id = 5, then saves or updates it in an Atlas-hosted MongoDB database. Thereafter, it displays the temperature readings from the database.

## Prerequisites

1. Ensure that `pymongo`, `pandas`, and `wirelesstagpy` are installed.
   
   Install via pip: `pip install pymongo pandas wirelesstagpy`

2. Create a `cred_tag.txt` containing the following:

    `[client_id]`  
    `[client_secret]`  
    `[redirect_url]`  
    `[username]`  
    `[password]`  
    `[atlasDbUrl]`  

## Usage

To run the script:

- python [script_name].py

- Replace `[script_name]` with the correct/chosen name of the script.

## Script Flow

1. Connect to the MongoDB Atlas database.
2. In a nested loop structure, fetch the sensor data three times, each with a 5-second interval, and store/update it in the MongoDB database. After each set of three observations, the script waits for 180 seconds before fetching data again.
3. Once all data fetching and updating is done, the script retrieves and displays the temperature readings stored in the database.

## Important Variables

- `NAME_`: The name value for the sensor record.
- `tag_id`: Currently set to 5. This is the sensor ID from which data is fetched.

## Functions

- `fetch_sensor_data()`: Fetches sensor data from wireless tags.
- `retrieve_sensor_data(atlasDbUrl)`: Retrieves sensor data from the MongoDB Atlas database and displays it.

## Notes

1. Ensure that the MongoDB Atlas database connection string in the `cred_tag.txt` file is correct and that the necessary permissions are granted.
2. Make sure the sensor with `tag_id` of 5 is active and transmitting data.

---

## Prototype - ipybn Google Colab Notebook

This section provides a brief overview of the Google Colab notebook which was used as a prototype to understand the integration with the wireless tag system. The script focuses on the authorisation process, fetching tag details, beeping a specific tag, and utilising the `wirelesstagpy` package to fetch various metrics from the tags.

### Prerequisites

1. Ensure you're running the script in a Jupyter-like environment, preferably Google Colab.
2. The script requires the `requests` and `wirelesstagpy` packages. These can be installed using pip.

### Steps

1. **Credentials**:
   - Read your credentials from `cred_tag.txt`.
   - Use these credentials to generate an authorisation URL.
   - Click on the displayed link to authorise the app and get the authorisation code.   
    <br>
    
2. **Authorisation Code**:
   - Once you have the authorisation code, input it into the script.
   - The script will then make a POST request to get an access token.
    <br><br>

1. **Fetching Tag Details**:
   - With the access token, make an API call to fetch the list of tags.
   - Display each tag's ID and name.
    <br> <br>

2. **Beeping a Tag**:
   - Input the ID of the tag you want to beep.
   - The script will then make an API call to beep the specified tag.
    <br><br>

3. **Using `wirelesstagpy`**:
   - Create a connection to the Wireless Sensor Tags platform.
   - Fetch the temperature, humidity, and other metrics from the specified tag every second for 10 seconds and store this data in a DataFrame.
   - Display the DataFrame after collecting the data.
    <br><br>

4. **Testing Various API Methods**:
   - Test various API methods like `GetTemperatureStats`, `GetGeneralEvents`, etc., to understand the different functionalities provided by the tag system API.
   - Display the status code for each API request.
   - For the `GetTemperatureStats` API method, process the temperature statistics into a DataFrame and display the first 20 rows.

### Notes

- This prototype script is a great way to understand the basic functionalities of the wireless tag system and how to integrate it into Python environments.
- Always ensure that you have the correct credentials and that the wireless tag system is active and online.