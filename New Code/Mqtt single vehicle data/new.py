import requests
import sqlite3
import json

# Adafruit IO credentials
IO_USERNAME = "Balajk123"
IO_KEY = "aio_TyMA06WL9hcVTSKnNyAn1bDdMZM7"

# Function to fetch data from Adafruit IO
def fetch_data():
    url = f"https://io.adafruit.com/api/v2/{IO_USERNAME}/feeds/vehicle"
    headers = {"X-AIO-Key": IO_KEY}

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            print("Fetched data:", data)  # Debugging: Print the fetched data
            return data
        else:
            print("Failed to fetch data from Adafruit IO:", response.status_code)
            return None
    except Exception as e:
        print("Error fetching data:", e)
        return None

# Function to store data in SQLite database
def store_data(data):
    if data:
        try:
            conn = sqlite3.connect('data.db')
            c = conn.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS vehicle_parameters
                         (id INTEGER PRIMARY KEY, type TEXT, latitude REAL, longitude REAL)''')

            # Extracting and parsing last_value
            last_value = data.get('last_value')
            if last_value:
                value_data = json.loads(last_value)
                if 'id' in value_data and 'latitude' in value_data and 'longitude' in value_data and 'altitude' in value_data:
                    c.execute('''INSERT INTO vehicle_parameters (id, type, latitude, longitude) VALUES (?, ?, ?, ?)''',
                              (value_data['id'], "car", value_data['latitude'], value_data['longitude']))
                    print("Data stored successfully.")
                else:
                    print("Invalid data format. Missing key(s) in 'value'.")
            else:
                print("No data found in 'last_value'.")
            
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            print("Error storing data in database:", e)

# Main function to fetch and store data
def main():
    data = fetch_data()
    if data:
        store_data(data)

if __name__ == "__main__":
    main()
