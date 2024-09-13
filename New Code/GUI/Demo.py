import os
import sys
import json
os.system("pyuic5 -o analoggaugewidget_demo_ui.py interface.ui")
import random
import serial
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtCore import QTimer, Qt
from analoggaugewidget_demo_ui import Ui_MainWindow
from analoggaugewidget import AnalogGaugeWidget
from Adafruit_IO import Client
import requests

# Define your Adafruit IO username and key
ADAFRUIT_IO_USERNAME = 'Balajk123'
ADAFRUIT_IO_KEY = 'aio_TyMA06WL9hcVTSKnNyAn1bDdMZM7'
FEED_NAME = 'vehicle'
TOLL_FEED_NAME = 'tollamount'
VEHICLE_PARAMETERS_FEED_NAME = 'VehicleParameters'

# Initialize the Adafruit IO client
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)
username = "Balajk123"
aio_key = "aio_TyMA06WL9hcVTSKnNyAn1bDdMZM7"
feed_key = "notifications"
toll_key = "tollamount"
vehicle_key = "vehicleparameters"
collision_key = "junction"

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setStyleSheet("background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #000000, stop:0.9 #000000, stop:1 #FF0000);")
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Initialize Serial Connection
        self.serial_port = 'COM7'  # Replace 'COMX' with your Arduino's serial port
        self.baud_rate = 9600  # Match this with your Arduino's baud rate
        try:
            self.ser = serial.Serial(self.serial_port, self.baud_rate)
        except serial.SerialException as e:
            print(f"Error opening serial port: {e}")
            sys.exit(1)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_numbers)
        self.timer.start(3000)  # Update every 1000 milliseconds (1 second)

        self.show()

    
    def update_numbers(self):
        try:
            if self.ser.in_waiting > 0:  # Read all available data in the buffer
                data = self.ser.readline().decode('utf-8').strip()
                print("Received data:", data)
                try:
                    json_data = json.loads(data)

                    rpm = json_data.get("rpm", "N/A")
                    voltage = json_data.get("voltage", "N/A")
                    temp = json_data.get("temp", "N/A")
                    soc = json_data.get("soc", "N/A")
                    #alert = json_data.get("alert", "N/A")
                    vehicle_id = json_data.get("id", "N/A")
                    latitude = json_data.get("lat", "N/A")
                    longitude = json_data.get("long", "N/A")
                    altitude = json_data.get("alt", "N/A")

                    self.ui.RPM.setText(str(rpm))
                    self.ui.Soc.setText(str(soc))
                    self.ui.Voltage.setText(str(voltage))
                    self.ui.Temp.setText(str(temp))

                    wheel_dia = 0.414
                    try:
                        speed = wheel_dia * float(rpm)
                    except ValueError:
                        speed = 0
                    self.ui.widget.updateValue(speed)

                
                    

                    data_payload = {
                        'id': vehicle_id,
                        'speed': rpm,
                        'latitude': latitude,
                        'longitude': longitude,
                        'altitude': altitude




                        
                    }

                    try:
                        adafruit_message = json.dumps(data_payload)
                        aio.send_data(FEED_NAME, adafruit_message)
                    except Exception as e:
                        print("Error sending data to Adafruit IO:", e)

                except json.JSONDecodeError as e:
                    print("Error decoding JSON:", e)

        except Exception as e:
            print("Error reading from serial port:", e)
        
        unit1 = '%'
        self.ui.RPM.setText(str(rpm))
        self.ui.RPM.setStyleSheet("color: white; background-color: black; font-size: 30px; font-family: 'Arial Black';")
        wheel_dia = 0.414
        speed = wheel_dia*rpm
        self.ui.widget.updateValue(speed)
        self.ui.Soc.setText(str(soc))
        self.ui.Soc.setStyleSheet("color: white; background-color: black; font-size: 30px; font-family: 'Arial Black';")

        self.ui.Voltage.setText(str(voltage))
        self.ui.Voltage.setStyleSheet("color:red ; background-color: black; font-size: 30px; font-family: 'Arial Black';")
        self.ui.Temp.setText(str(temp))
        self.ui.Temp.setStyleSheet("color: white; background-color: black; font-size: 30px; font-family: 'Arial Black';")




def fetch_data():
    try:
        fetch_feed_data(feed_key)
        fetch_feed_data(toll_key)
        fetch_feed_data(vehicle_key)
        fetch_feed_data(collision_key)
    except Exception as e:
        print("An error occurred during data fetch:", str(e))

def fetch_feed_data(feed_name):
    try:
        url = f"https://io.adafruit.com/api/v2/{username}/feeds/{feed_name}/data"
        response = requests.get(url, headers={"X-AIO-Key": ADAFRUIT_IO_KEY})

        if response.status_code == 200:
            data = response.json()
            print(f"Received data from Adafruit IO feed '{feed_name}':", data)

            if feed_name == 'tollamount':
                for entry in data:
                    value = int(entry['value'])
                    show_notification_popup(f"Toll amount received: {entry['value']}")

            elif feed_name == 'notifications':
                for entry in data:
                    notification_value = entry['value']
                    if 'Car1' in notification_value:
                        print(notification_value)
                        show_notification_popup(f"Car 1 detected: {notification_value}")
                    

            elif feed_name == 'vehicleparameters':
                for entry in data:
                    vehicle_params = entry['value']
                    # Check for specific conditions in vehicle parameters
                    
                    show_notification_popup(f"Emergency vehicle detected: {vehicle_params}")
            elif feed_name == 'junction':
                for entry in data:
                    junction_value = entry['value']
                    if 'Car1' in junction_value:
                        print(junction_value)
                        show_notification_popup(f"{junction_value}")

        else:
            print(f"Error: Failed to fetch data from Adafruit IO feed '{feed_name}', status code: {response.status_code}")

    except Exception as e:
        print(f"An error occurred during data fetch for feed '{feed_name}':", str(e))


def show_notification_popup(notification_value):
    try:
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setWindowTitle("Notification")
        msg_box.setText(notification_value)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.setStyleSheet("""
            QMessageBox {
                background-color: #000000;
                border: none;
            }
            QLabel {
                color: white;
                min-width: 300px;
            }
        """)
        msg_box.setWindowFlags(msg_box.windowFlags() | Qt.FramelessWindowHint)
        msg_box.exec_()
    except Exception as e:
        print("An error occurred while displaying popup:", str(e))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()

    # Create a QTimer to fetch data every 5 seconds
    timer = QTimer()
    timer.timeout.connect(fetch_data)
    timer.start(5000)  # Interval in milliseconds (5 seconds)

    # Initial fetch of data
    fetch_data()

    sys.exit(app.exec_())
