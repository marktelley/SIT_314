import pymongo
import time
import pandas as pd
import wirelesstagpy
import matplotlib.pyplot as plt

# Key variable - Name Value for Sensor Record
NAME_ = "SIT_314_TEST"

# Read credentials from file
with open('cred_tag.txt', 'r') as file:
    lines = file.readlines()
    client_id = lines[0].strip()
    client_secret = lines[1].strip()
    redirect_url = lines[2].strip()
    username_ = lines[3].strip()
    password_ = lines[4].strip()
    atlasDbUrl = lines[5].strip()


# GET data FROM API and POST to MongoDB
def fetch_sensor_data():
    api = wirelesstagpy.WirelessTags(username=username_, password=password_)
    tags = api.load_tags()

    for (uuid, tag) in tags.items():
        if tag.tag_id == 5:
            update_data = {
                "query": {"name": NAME_},
                "push_data": {
                    "time": pd.Timestamp.now().isoformat(),
                    "temperature": tag.temperature,
                },
                "set_on_insert": {
                    "name": NAME_,
                    "address": "321 Deakin Uni, Burwood VIC 3125"
                }
            }
            return update_data
    return None

# GET DATA from Atlas and return as a list
def retrieve_sensor_data(atlasDbUrl):
    import pymongo

    client = pymongo.MongoClient(atlasDbUrl)
    db = client['Atlas']
    sensor_collection = db['sensors']
    sensor_data = sensor_collection.find_one({"name": NAME_})

    temperature_readings = []

    if not sensor_data:
        print("No data found")
        client.close()
        return temperature_readings

    print("Temperature Readings:")
    if 'sensorData' in sensor_data:
        for reading in sensor_data['sensorData']:
            print(reading['temperature'])
            temperature_readings.append(reading['temperature'])
    else:
        print("No sensor data in document")

    client.close()
    return temperature_readings

# Plot temperature data
def plot_temperature_data(temp_data):
    plt.plot(temp_data)
    plt.xlabel("Reading Index")
    plt.ylabel("Temperature (°C)")
    plt.title("Temperature Readings")
    plt.show()


def main():
    try:
        client = pymongo.MongoClient(atlasDbUrl)
        db = client['Atlas']
        sensor_collection = db['sensors']
        print(f"Connected to MongoDB database: Atlas")
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return

    # Nested loop for multiple observations within each main iteration
    for _ in range(3):
        for _ in range(3):  # 3 observations
            sensordata = fetch_sensor_data()

            if sensordata:
                result = sensor_collection.update_one(sensordata["query"],
                                                      {"$push": {"sensorData": sensordata["push_data"]},
                                                       "$setOnInsert": sensordata["set_on_insert"]},
                                                      upsert=True)
                if result.upserted_id:
                    print(f"Created new document with ID: {result.upserted_id}")
                else:
                    print(f"Updated existing document.")
            else:
                print(f"No data fetched for iteration {_}")

            time.sleep(5)  # Wait for 5 seconds before the next observation
        time.sleep(180) # Wait 180 seconds before next read.

    client.close()
    temperature_data = retrieve_sensor_data(atlasDbUrl)
    if temperature_data:
        plot_temperature_data(temperature_data)


if __name__ == "__main__":
    main()