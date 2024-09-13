import sqlite3
import requests
import json
import time

# Function to fetch data from SQLite database
def fetch_data_from_db():
    # Connect to the database
    conn = sqlite3.connect('vehicle_data.db')
    cursor = conn.cursor()

    # Fetch total number of vehicle data
    cursor.execute("SELECT COUNT(*) FROM VehicleData")
    total_vehicles = cursor.fetchone()[0]

    # Fetch total number of ambulances
    cursor.execute("SELECT COUNT(*) FROM VehicleData WHERE vehicle_type = 'ambulance'")
    ambulances = cursor.fetchone()[0]

    # Fetch total number of fire engines
    cursor.execute("SELECT COUNT(*) FROM VehicleData WHERE vehicle_type = 'fire engine'")
    fire_engines = cursor.fetchone()[0]

    # Close the connection
    conn.close()

    return total_vehicles, ambulances, fire_engines

# Your Adafruit IO username and active key
username = "***************"
active_key = "***************"

# URL of the feed
url = f"https://io.adafruit.com/api/v2/{username}/feeds/vehicleparameters/data"

# Headers with authorization
headers = {
    "X-AIO-Key": active_key,
    "Content-Type": "application/json"
}

# Main loop to fetch data and publish it every 5 seconds
while True:
    # Fetching data from the database
    total_vehicles, ambulances, fire_engines = fetch_data_from_db()

    # Calculate total number of ambulances and fire engines
    total_ambulance_fire_engine = ambulances + fire_engines

    # Construct the data dictionary with the required format
    data = {
        "id": "0FJ9SBK1PPAMXX2M36007GNNSS",
        "value": total_ambulance_fire_engine  # Assign the sum of ambulances and fire engines here
    }

    # Convert data to JSON format
    json_data = json.dumps(data)

    # Sending POST request to publish data
    response = requests.post(url, headers=headers, data=json_data)

    # Checking response status
    if response.status_code == 200:
        print("Data published successfully!")
    else:
        print("Failed to publish data. Status code:", response.status_code)
        print("Response:", response.text)

    # Print total vehicle, total ambulance, and total fire engine
    print(f"Total Vehicles: {total_vehicles}")
    print(f"Total Ambulances: {ambulances}")
    print(f"Total Fire Engines: {fire_engines}")

    # Sleep for 5 seconds before fetching and publishing data again
    time.sleep(5)
