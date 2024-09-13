import sqlite3
from Adafruit_IO import Client

class CurvatureRoad:
    def __init__(self, regions):
        self.regions = regions
        self.vehicles_in_region1 = set()
        self.vehicles_in_region3 = set()
        self.messages_sent = set()
        self.aio = Client("***************", "***************")  # Replace with your Adafruit IO username and key

    def check_vehicle_position(self, vehicle_data):
        for vehicle in vehicle_data:
            car = vehicle['car']
            readings = vehicle['readings']
            message_sent = False

            for lat, lon, _ in readings:
                for region, limits in self.regions.items():
                    lower_limit_lon = float(limits['lower_limit_lon'])
                    upper_limit_lon = float(limits['upper_limit_lon'])
                    lower_limit_lat = float(limits['lower_limit_lat'])
                    upper_limit_lat = float(limits['upper_limit_lat'])

                    if lower_limit_lon <= lon <= upper_limit_lon and lower_limit_lat <= lat <= upper_limit_lat:
                        if region == '1':
                            self.vehicles_in_region1.add(car)
                        elif region == '3':
                            self.vehicles_in_region3.add(car)
                    elif region == '2':
                        if car in self.vehicles_in_region1 and car not in self.messages_sent:
                            self.messages_sent.add(car)
                            self.aio.send('notifications', f'{car}: Another vehicle on the opposite side.')
                        elif car in self.vehicles_in_region3 and car not in self.messages_sent:
                            self.messages_sent.add(car)
                            self.aio.send('notifications', f'{car}: Another vehicle on the opposite side.')

# Connect to the database
conn = sqlite3.connect('vehicle_data1.db')
cursor = conn.cursor()

# Execute a query to fetch vehicle data
cursor.execute("SELECT car, lat, lon, speed FROM vehicles")

# Fetch all rows from the result set
rows = cursor.fetchall()

# Close the connection
conn.close()

# Prepare vehicle_data list
vehicle_data = []

# Process fetched data into the required format
for row in rows:
    car, lat, lon, speed = row
    readings = [(lat, lon, speed) for _ in range(5)]  # Assuming 5 readings per vehicle
    vehicle_data.append({"car": car, "readings": readings})

# Define regions
regions = {
    "1": {
        "lower_limit_lon": "76.903614",
        "upper_limit_lon": "76.903636",
        "lower_limit_lat": "10.903805",
        "upper_limit_lat": "10.903834"
    },
    "2": {
        "lower_limit_lon": "76.903898",
        "upper_limit_lon": "76.903924",
        "lower_limit_lat": "10.903749",
        "upper_limit_lat": "10.903767"
    },
    "3": {
        "lower_limit_lon": "76.903951",
        "upper_limit_lon": "76.903982",
        "lower_limit_lat": "10.903615",
        "upper_limit_lat": "10.903625"
    }
}

# Now you have vehicle_data ready, proceed with your existing code
road = CurvatureRoad(regions)
road.check_vehicle_position(vehicle_data)
