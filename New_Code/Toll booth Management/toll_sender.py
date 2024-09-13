import time
from Adafruit_IO import Client, Feed

# Adafruit IO username and active key
ADAFRUIT_IO_USERNAME = '***************'
ADAFRUIT_IO_KEY = '***************'

# Create an instance of the REST client
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

# Create a feed
feed = aio.feeds('tolldata')

# Data to be published
data = [
    (0, 40), (0, 39), (0, 38), (0, 37), (0, 36), (0, 35), (0, 34), (0, 33), (0, 32), (0, 31),
    (0, 30), (0, 29), (0, 28), (0, 27), (0, 26), (0, 25), (0, 24), (0, 23), (0, 22), (0, 21),
    (0, 20), (0, 19), (0, 18), (0, 18), (0, 17), (0, 16), (0, 15), (0, 14), (0, 13), (0, 12),
    (0, 11), (0, 10), (0, 9), (0, 8), (0, 7), (0, 6), (0, 5), (0, 4), (0, 3), (0, 2), (0, 1),
    (0, 0), (0, -1), (0, -2), (0, -3), (0, -6), (0, -9), (0, -10), (0, -20), (0, -20), (-1, -25),
    (-2, -25), (-4, -25), (-5, -25), (-6, -25), (-7, -25)
]

# Reverse the order of the data pairs
data.reverse()

# Publish data
for value in data:
    aio.send_data(feed.key, str(value))
    time.sleep(2)  # Delay to avoid rate limits

print("Data published successfully.")
