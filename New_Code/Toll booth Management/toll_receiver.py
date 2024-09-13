import requests

# Adafruit IO credentials
username = "Balajk123"
aio_key = "aio_TyMA06WL9hcVTSKnNyAn1bDdMZM7"
feed_key = "tolldata"

# URL to fetch data from Adafruit IO feed
url = f"https://io.adafruit.com/api/v2/{username}/feeds/{feed_key}/data"

try:
    # Fetch data from the feed
    response = requests.get(url, headers={"X-AIO-Key": aio_key})

    # Check if request was successful
    if response.status_code == 200:
        # Extract data from the response
        data = response.json()

        # Open file for writing
        with open("movement2.txt", "w") as file:
            # Write each data point to the file
            for entry in data:
                file.write(f"{entry['value']}\n")

        print("Data has been successfully written.")
    else:
        print("Failed to fetch data. Status code:", response.status_code)

except Exception as e:
    print("An error occurred:", str(e))
