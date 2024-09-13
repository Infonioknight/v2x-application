import numpy as np
import matplotlib.pyplot as plt
import time
import tkinter as tk
from Adafruit_IO import Client

class Vehicle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.wallet = 1000  
        self.total_toll_amount = 0  
        self.distance_traveled = 0  
        self.aio = Client('***************', '***************') 

    def move(self, filename='movement2.txt'):
        with open(filename, 'r') as file:
            movements = file.readlines()

        for movement in movements:
            if movement.strip() == 'stop':
                print("Vehicle stopped.")
                break  

            coords = eval(movement.strip())  
            if not isinstance(coords, tuple) or len(coords) != 2:
                print("Invalid movement format.")
                return

            self.x, self.y = coords  
            self.update_vehicle_plot()  
            self.check_toll_booth()  
            time.sleep(0.25)  

        print("Movement finished.")
        self.publish_to_adafruit_io()  

    def check_toll_booth(self):
        if self.y == 0 or self.y == -30:
            self.pay_toll()
        elif self.x == -2:
            if self.y == -10:
                self.pay_toll(25)
            elif self.y == -20:
                self.pay_toll(50)
            elif self.y == -25:
                self.pay_toll(75)
            elif self.y == -10:  
                self.pay_toll(25)

    def pay_toll(self, amount=100):
        if self.wallet >= amount:
            self.wallet -= amount  # Deduct the toll amount
            self.total_toll_amount += amount  # Update total toll amount
            self.update_wallet_display()  # Update wallet display
            print(f"Toll paid. Rs. {amount} deducted from the wallet.")
            print(f"Remaining balance: Rs. {self.wallet}")
        else:
            print("Insufficient funds to pay toll.")

    def update_vehicle_plot(self):
        plt.figure(1, figsize=(8, 6))  # Larger figure size for vehicle movement
        plt.clf()
        plt.xlim(-5, 5)
        plt.ylim(-40, 40)
        plt.scatter(self.x, self.y, color='blue', label='Vehicle', s=100)  # Adjust size here (s=100)
        plt.plot([-5, 5], [0, 0], color='red', linestyle='-')  # Horizontal line representing the toll booth at y=0
        plt.plot([-5, 5], [-30, -30], color='red', linestyle='-')  # Horizontal line representing the toll booth at y=-30
        plt.legend()
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title('Vehicle Movement')
        plt.grid(True)
        plt.pause(0.01)

    def update_wallet_display(self):
        updated_toll_amount = 1000 - self.wallet
        wallet_label.config(text=f' Toll amount: Rs. {updated_toll_amount}', font=('Helvetica', 20))  
        root.update()  

    def publish_to_adafruit_io(self):
        self.aio.send('tollamount', self.total_toll_amount)


root = tk.Tk()
root.title("Toll amount Dashboard")
root.geometry("400x150")  


wallet_label = tk.Label(root, text=f' Toll amount: Rs. 0', font=('Helvetica', 20))  # Larger font size
wallet_label.pack()


vehicle = Vehicle(0, 0)


vehicle.move()
