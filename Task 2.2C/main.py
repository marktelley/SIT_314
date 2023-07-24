import asyncio
from bleak import BleakClient
import pandas as pd
from cycling_power_service import CyclingPowerService
from datetime import datetime
from google.cloud import bigquery
from google.cloud.bigquery import Table
import os
import warnings

# Settings the warnings to be ignored
warnings.filterwarnings('ignore')

# Define the length of the data collection session (in seconds)
session_length = 30.0

# Define the device address (replace with your device address; use discover.py to get address)
device_address = "XX:XX:XX:XX:XX:XX"

# Define an async function for running the data collection
async def run(address, session_length):
    data_list = []  # Create an empty list to store the data points
    previous_data = {'cumulative_crank_revs': 0, 'last_crank_event_time': 0}

    async with BleakClient(address) as client:
        def data_handler(data):
            nonlocal previous_data
            formatted_step = datetime.now().strftime("%Y/%m/%d %H:%M:%S")

            delta_revs = data.cumulative_crank_revs - previous_data['cumulative_crank_revs']
            delta_time = (data.last_crank_event_time - previous_data['last_crank_event_time']) & 0xFFFF

            cadence = (delta_revs / delta_time * 60 * 1024) if delta_time > 0 else 0  # Calculate the cadence (in rpm)

            data_list.append({
                'step': formatted_step,
                'instantaneous_power': data.instantaneous_power,
                'accumulated_energy': data.accumulated_energy,
                'accumulated_torque': data.accumulated_torque,
                'cumulative_wheel_revs': data.cumulative_wheel_revs,
                'last_wheel_event_time': data.last_wheel_event_time,
                'cumulative_crank_revs': data.cumulative_crank_revs,
                'last_crank_event_time': data.last_crank_event_time,
                'maximum_force_magnitude': data.maximum_force_magnitude,
                'minimum_force_magnitude': data.minimum_force_magnitude,
                'maximum_torque_magnitude': data.maximum_torque_magnitude,
                'minimum_torque_magnitude': data.minimum_torque_magnitude,
                'top_dead_spot_angle': data.top_dead_spot_angle,
                'bottom_dead_spot_angle': data.bottom_dead_spot_angle,
                'cadence': cadence
            })

            previous_data = {'cumulative_crank_revs': data.cumulative_crank_revs, 'last_crank_event_time': data.last_crank_event_time}

            print(f'Power (w): {data.instantaneous_power}, Cadence (rpm): {cadence}')  # Print power and cadence

        await client.is_connected()  # Ensure the client is connected
        trainer = CyclingPowerService(client)
        trainer.set_cycling_power_measurement_handler(data_handler)
        await trainer.enable_cycling_power_measurement_notifications()
        await asyncio.sleep(session_length)
        await trainer.disable_cycling_power_measurement_notifications()

    df = pd.DataFrame(data_list)  # Create a pandas dataframe from the data list
    df.to_csv("Activity_Data.csv")  # Save the dataframe to a CSV file
    df['step'] = pd.to_datetime(df['step'], format='%Y/%m/%d %H:%M:%S')  # Parse 'step' as a datetime object

    # Instantiate a BigQuery client
    client = bigquery.Client.from_service_account_json('XXXXXX-XXXXXX-XXXXXX.json')

    # Specify dataset and table
    table_id = "XXXXXXX-XXXXXXXXX.example.activity"

    # Create the table if it doesn't exist
    try:
        client.get_table(table_id)  # Make an API request/overwrite data is table exists
    except Exception as e:
        table = Table(table_id)
        client.create_table(table)

    # Create the table and load data
    job_config = bigquery.LoadJobConfig(autodetect=True, write_disposition='WRITE_TRUNCATE')
    job = client.load_table_from_dataframe(df, table_id, job_config=job_config)

    # Ensure the data load job completes without errors
    job.result()

    print(df)

if __name__ == "__main__":
    os.environ["PYTHONASYNCIODEBUG"] = str(1)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(device_address, session_length))
