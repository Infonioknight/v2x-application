import math
import sqlite3
import time
from Adafruit_IO import Client

# Define your Adafruit IO username and key
ADAFRUIT_IO_USERNAME = '***************'
ADAFRUIT_IO_KEY = '***************'

# Define the feed name
FEED_NAME = 'junction'

# Initialize the Adafruit IO client
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

def calculate_cartesian_distance(lat1, lon1, lat2, lon2):
    """Calculate the Cartesian distance between two points on Earth."""
    x_distance = (lon2 - lon1) * math.cos(0.5 * (lat2 + lat1))
    y_distance = lat2 - lat1
    distance = math.sqrt(x_distance ** 2 + y_distance ** 2)
    return distance

def check_approaching(previous_distance, current_distance):
    """Check if the vehicle is approaching or leaving."""
    if current_distance < previous_distance:
        return "Approaching"
    elif current_distance > previous_distance:
        return "Leaving"
    else:
        return None  # No change

def calculate_approaching_count(vehicle_data, target_point, approaching_time_difference, regions):
    """Calculate the number of approaching vehicles within the specified time difference."""
    approaching_counts = {}
    for vehicle in vehicle_data:
        last_reading = vehicle["readings"][-1]  
        lat, lon = last_reading[:2]  
        current_distance = calculate_cartesian_distance(lat, lon, target_point[0], target_point[1])
        previous_distance = None
        approach_status = None
        vehicle_region = None  
        if len(vehicle["readings"]) > 1:
            lat, lon = vehicle["readings"][-2][:2]  
            previous_distance = calculate_cartesian_distance(lat, lon, target_point[0], target_point[1])
            approach_status = check_approaching(previous_distance, current_distance)
            
            # Determine the region of the current vehicle
            for region, limits in regions.items():
                if float(limits["lower_limit_lon"]) <= lon <= float(limits["upper_limit_lon"]) and \
                   float(limits["lower_limit_lat"]) <= lat <= float(limits["upper_limit_lat"]):
                    vehicle_region = region
                    break

        if approach_status == "Approaching":
            approaching_directions = {}  
            for other_vehicle in vehicle_data:
                if other_vehicle["id"] != vehicle["id"]:  
                    other_last_reading = other_vehicle["readings"][-1]
                    other_lat, other_lon = other_last_reading[:2]  
                    other_current_distance = calculate_cartesian_distance(other_lat, other_lon, target_point[0], target_point[1])
                    if len(other_vehicle["readings"]) > 1:
                        other_previous_distance = calculate_cartesian_distance(other_vehicle["readings"][-2][0], other_vehicle["readings"][-2][1], target_point[0], target_point[1])
                        other_approach_status = check_approaching(other_previous_distance, other_current_distance)
                        if other_approach_status == "Approaching" and abs(current_distance - other_current_distance) <= approaching_time_difference:
                            other_vehicle_region = None
                            for region, limits in regions.items():
                                if float(limits["lower_limit_lon"]) <= other_lon <= float(limits["upper_limit_lon"]) and \
                                   float(limits["lower_limit_lat"]) <= other_lat <= float(limits["upper_limit_lat"]):
                                    other_vehicle_region = region
                                    break
                            if other_vehicle_region == "5":
                                other_vehicle_region = str(int(other_vehicle_region) - 1)
                            if vehicle_region:
                                approaching_counts.setdefault(vehicle["id"], {"count": 0, "approaching_from": {}, "current_vehicle_region": vehicle_region})["count"] += 1
                                approaching_counts[vehicle["id"]]["approaching_from"].setdefault(other_vehicle_region, 0)
                                approaching_counts[vehicle["id"]]["approaching_from"][other_vehicle_region] += 1
                            else:
                                approaching_counts.setdefault(vehicle["id"], {"count": 0, "approaching_from": {}, "current_vehicle_region": None})["count"] += 1
                                approaching_counts[vehicle["id"]]["approaching_from"].setdefault(other_vehicle_region, 0)
                                approaching_counts[vehicle["id"]]["approaching_from"][other_vehicle_region] += 1

    return approaching_counts

def fetch_vehicle_data_from_db(database_path):
    """Fetch vehicle data from the database."""
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    cursor.execute("SELECT car, lat, lon, speed FROM vehicles")
    vehicle_data = {}
    for row in cursor.fetchall():
        car, lat, lon, _ = row
        if car in vehicle_data:
            vehicle_data[car]["readings"].append((lat, lon))
        else:
            vehicle_data[car] = {"id": car, "readings": [(lat, lon)]}
    conn.close()
    return list(vehicle_data.values())

# Target point
target_point = (10.903669, 76.808849)

# Regions data
regions = {
  "1": {
    "lower_limit_lon": "76.898863",
    "upper_limit_lon": "76.898950",
    "lower_limit_lat": "10.903652",
    "upper_limit_lat": "10.903682"
  },
  "2": {
    "lower_limit_lon": "76.898828",
    "upper_limit_lon": "76.898863",
    "lower_limit_lat": "10.903589",
    "upper_limit_lat": "10.903682"
  },
  "3": {
    "lower_limit_lon": "76.898696",
    "upper_limit_lon": "76.898828",
    "lower_limit_lat": "10.903652",
    "upper_limit_lat": "10.903682"
  },
  "4": {
    "lower_limit_lon": "76.898828",
    "upper_limit_lon": "76.898863",
    "lower_limit_lat": "10.903682",
    "upper_limit_lat": "10.903727"
  },
 "5": {
    "lower_limit_lon": "76.898828",
    "upper_limit_lon": "76.898863",
    "lower_limit_lat": "10.903652",
    "upper_limit_lat": "10.903682"
    }
  }

# Define time difference for approaching vehicles
approaching_time_difference = 3  # Seconds

# Directions between regions
directions = {
    "1": {"left": "2", "straight": "3", "right": "4"},
    "2": {"left": "3", "straight": "4", "right": "1"},
    "3": {"left": "4", "straight": "1", "right": "2"},
    "4": {"left": "1", "straight": "2", "right": "3"}
}

# Function to send data to Adafruit IO
def send_to_adafruit(vehicle_id, approaching_counts):
    for vehicle_id, info in approaching_counts.items():
        current_region = info.get('current_vehicle_region', None)
        other_region_counts = info.get('approaching_from', None)
        
        if current_region and other_region_counts:  # Ensure regions and approaching counts are available
            message = f"{vehicle_id} : Another Vehicle is approaching from:\n"
            for other_region, count in other_region_counts.items():
                current_direction = next(direction for direction, region in directions[current_region].items() if region == other_region)
                message += f" - {current_direction}: {count} vehicle(s)\n"
            # Send message to Adafruit IO feed
            aio.send(FEED_NAME, message)
        else:
            message = f"{vehicle_id} is not approaching any other vehicle within {approaching_time_difference} seconds."
            # Send message to Adafruit IO feed
            aio.send(FEED_NAME, message)

# Main function
def main():
    # Fetch vehicle data from the database
    vehicle_data = fetch_vehicle_data_from_db("vehicle_data1.db")

    # Calculate the number of approaching vehicles within the specified time difference
    approaching_counts = calculate_approaching_count(vehicle_data, target_point, approaching_time_difference, regions)

    # Send approaching counts to Adafruit IO
    send_to_adafruit(vehicle_data, approaching_counts)

# Execute the main function
if __name__ == "__main__":
    main()
