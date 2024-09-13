import tkinter as tk
from tkinter import filedialog, messagebox, Menu
import matplotlib.pyplot as plt
from shapely.geometry import Point, Polygon
import sqlite3
import logging
import os
import hashlib
import webbrowser

class TrafficLightApp:
    def __init__(self, master):
        self.master = master
        master.title("Traffic Light Controller")

     
        self.conn = sqlite3.connect("data.db")
        self.cursor = self.conn.cursor()

        
        self.vehicle_visibility = {vehicle_type: tk.BooleanVar(value=True) for vehicle_type in ["car", "ambulance", "fire_engine", "cab", "bike"]}

      
        self.create_widgets()
        self.set_fixed_sizes()
        self.populate_junction_buttons()
        self.create_menu()

    
        self.detect_vehicles()

    def create_widgets(self):
        self.label = tk.Label(self.master, text="Select Junction:", pady=10, font=("Arial", 12, "bold"), fg="blue")
        self.label.grid(row=0, column=0, columnspan=2, padx=10)  

        self.result_frame = tk.Frame(self.master, bg="lightgreen")
        self.result_frame.grid(row=0, column=3, rowspan=5, padx=10)

        self.feedback_button = tk.Button(self.master, text="Report Issue", command=self.open_feedback_link, width=15, height=3, bg="green", fg="white")
        self.feedback_button.grid(row=6, column=0, padx=30, pady=30)

        self.chatbot_button = tk.Button(self.master, text="Chat", command=self.open_chatbot, width=15, height=3, bg="blue", fg="white")
        self.chatbot_button.grid(row=7, column=0, padx=30, pady=10)

    def set_fixed_sizes(self):
        self.box_width = 15
        self.header_height = 2
        self.result_height = 2

    def populate_junction_buttons(self):
        self.junction_buttons = []
        for i, junction_name in enumerate(["Junction 1", "Junction 2", "Junction 3"]):
            button = tk.Button(self.master, text=junction_name, command=lambda name=junction_name: self.select_junction(name), width=15, height=3, bg="yellow", fg="black")
            button.grid(row=i+1, column=0, pady=5, padx=10)
            self.junction_buttons.append(button)

    def create_menu(self):
        menubar = Menu(self.master)
        self.master.config(menu=menubar)

        file_menu = Menu(menubar, tearoff=0)
        file_menu.add_command(label="Exit", command=self.master.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        view_menu = Menu(menubar, tearoff=0)
        for vehicle_type, var in self.vehicle_visibility.items():
            view_menu.add_checkbutton(label=f"Show {vehicle_type.capitalize()}", variable=var, command=self.detect_vehicles)
        menubar.add_cascade(label="View", menu=view_menu)

        help_menu = Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=self.display_about_info)
        menubar.add_cascade(label="Help", menu=help_menu)

    def select_junction(self, junction_name):
        self.selected_junction = junction_name
        self.label.config(text=f" {junction_name}")
        logging.info(f"Selected Junction {junction_name}")
        self.detect_vehicles()

    def display_about_info(self):
        about_text = "Traffic Light Controller\n\nVersion: 1.0\nAuthor: Hector\n\nA simple traffic light controller application."
        messagebox.showinfo("About", about_text)

    def detect_vehicles(self):
        lane_coordinates_list = [
            Polygon([(0, 40), (0, 20), (20, 20), (20, 40)]),
            Polygon([(20, 0), (40, 0), (40, -20), (20, -20)]),
            Polygon([(0, -20), (0, -40), (-20, -40), (-20, -20)]),
            Polygon([(-20, 0), (-40, 0), (-40, 20), (-20, 20)])
        ]

        results = []

        for i, lane_polygon in enumerate(lane_coordinates_list):
            lane_number = (i + 1) * 2  # Calculate the lane number

            self.cursor.execute("SELECT * FROM vehicle_parameters")
            vehicle_data = self.cursor.fetchall()

            vehicle_counts = {vehicle_type: 0 for vehicle_type in ["car", "ambulance", "fire_engine", "cab", "bike"]}
            priority = ""
            green_light_time = 5

            for data in vehicle_data:
                identity, latitude, longitude = data[1:]
                vehicle_point = Point(float(latitude), float(longitude))

                if vehicle_point.within(lane_polygon):
                    identity_lower = identity.lower()
                    if identity_lower in vehicle_counts and self.vehicle_visibility[identity_lower].get():
                        vehicle_counts[identity_lower] += 1

            if vehicle_counts["ambulance"] > 0:
                priority = "Ambulance detected"
                green_light_time = 60
            elif vehicle_counts["fire_engine"] > 0:
                priority = "Fire Engine detected"
                green_light_time = 60
            else:
                total_cars = sum(vehicle_counts.values())
                if total_cars <= 5:
                    green_light_time = 15
                elif 5 < total_cars <= 15:
                    green_light_time = 30
                else:
                    green_light_time = 60

            result_values = [f"Lane {lane_number}", vehicle_counts["car"], vehicle_counts["ambulance"],
                             vehicle_counts["fire_engine"], vehicle_counts["cab"], vehicle_counts["bike"],
                             priority, f"{green_light_time} seconds"]

            results.append(result_values)

        self.update_gui(lane_coordinates_list, results)

    def update_gui(self, lane_coordinates_list, results):
        plt.close('all')
        for widget in self.result_frame.winfo_children():
            widget.destroy()

        result_label = tk.Label(self.result_frame, text="Results", font=("Arial", 16, "bold"), pady=10, bg="lightgreen")
        result_label.grid(row=0, column=0, columnspan=8)

        headers = ["Lane", "Cars", "Ambulances", "Fire Engines", "Cabs", "Bikes", "Priority", "Green Light Time"]
        for col, header in enumerate(headers):
            header_label = tk.Label(self.result_frame, text=header, font=("Arial", 12, "bold"), width=self.box_width,
                                    height=self.header_height, padx=10, pady=5, relief=tk.GROOVE, bg="lightblue")
            header_label.grid(row=1, column=col)

        fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(10, 4))  # Adjust figsize here
        axes = axes.flatten()

        legend_items = []  # Create legend items

        for i, (lane_polygon, result_values) in enumerate(zip(lane_coordinates_list, results)):
            lane_number = (i + 1) * 2  # Calculate the lane number

            for col, value in enumerate(result_values):
                result_label = tk.Label(self.result_frame, text=value, width=self.box_width,
                                        height=self.result_height, padx=10, pady=5, relief=tk.RIDGE, bg="lightyellow")
                result_label.grid(row=i + 2, column=col)

            axes[i].set_title(f"Lane {lane_number}")
            axes[i].set_aspect('equal', 'box')
            axes[i].set_axis_off()

            x, y = lane_polygon.exterior.xy
            axes[i].fill(x, y, color='gray', alpha=0.5)

            self.cursor.execute("SELECT * FROM vehicle_parameters")
            vehicle_data = self.cursor.fetchall()

            for data in vehicle_data:
                identity, latitude, longitude = data[1:]
                vehicle_point = Point(float(latitude), float(longitude))

                if vehicle_point.within(lane_polygon):
                    color = 'green' if identity.lower() == 'bike' else ('red' if identity.lower() in ['ambulance', 'fire_engine'] else 'blue')
                    marker = 's' if identity.lower() == 'car' else 'o'  
                    marker_size = 50 if identity.lower() == 'car' else 30  
                    axes[i].scatter(float(latitude), float(longitude), color=color, marker=marker, s=marker_size)

                    # Add legend items for each type of vehicle if not already added
                    if identity.lower() == 'car':
                        if 'Car' not in [item.get_label() for item in legend_items]:
                            legend_items.append(plt.Line2D([0], [0], marker='s', color='w', label='Car', markerfacecolor='blue', markersize=10))
                    elif identity.lower() == 'bike':
                        if 'Bike' not in [item.get_label() for item in legend_items]:
                            legend_items.append(plt.Line2D([0], [0], marker='o', color='w', label='Bike', markerfacecolor='green', markersize=10))
                    elif identity.lower() == 'cab':
                        if 'Cab' not in [item.get_label() for item in legend_items]:
                            legend_items.append(plt.Line2D([0], [0], marker='o', color='w', label='Cab', markerfacecolor='blue', markersize=10))
                    elif identity.lower() in ['ambulance', 'fire_engine']:
                        if 'Emergency Vehicle' not in [item.get_label() for item in legend_items]:
                            legend_items.append(plt.Line2D([0], [0], marker='o', color='w', label='Emergency Vehicle', markerfacecolor='red', markersize=10))

        plt.tight_layout()

        # Place the legend in the upper right corner outside the plot area
        fig.subplots_adjust(right=0.8)
        axes[0].legend(handles=legend_items, loc='center left', bbox_to_anchor=(3.5, 0.5)) 

        plt.show()
        plt_manager = plt.get_current_fig_manager()
        plt_manager.window.wm_geometry("+{}+{}".format(self.master.winfo_x() + self.master.winfo_width() - plt_manager.window.winfo_width(), 
                                                   self.master.winfo_y() + self.master.winfo_height() - plt_manager.window.winfo_height()))

    def open_feedback_link(self):
        feedback_link = "https://respond.forms.app/cyberhector/feedback-form"
        webbrowser.open_new(feedback_link)

    def open_chatbot(self):
        chatbot_window = tk.Toplevel(self.master)
        chatbot_window.title("Chatbot")
        chatbot_window.geometry("600x800") 
        chatbot_window.resizable(False, False)

        chat_frame = tk.Frame(chatbot_window)
        chat_frame.pack(fill=tk.BOTH, expand=True)

        chat_text = tk.Text(chat_frame, wrap=tk.WORD, height=25) 
        chat_text.pack(fill=tk.BOTH, expand=True)
        chat_text.insert(tk.END, "Chatbot: Hi, what is the issue?\n\n")

        user_input_entry = tk.Text(chat_frame, wrap=tk.WORD, height=5)  
        user_input_entry.pack(side=tk.TOP, fill=tk.X, pady=10)  

        send_button = tk.Button(chat_frame, text="Send", command=lambda: self.send_message(chat_text, user_input_entry, chatbot_window))
        send_button.pack(side=tk.BOTTOM, pady=10)  

    def send_message(self, chat_text, user_input_entry, chatbot_window):
        message = user_input_entry.get("1.0", "end-1c")
        if "problem" in message.lower():
            chat_text.insert(tk.END, f"You: {message}\n\n")
            chat_text.insert(tk.END, "Chatbot: I'm sorry to hear that. Please report your issue through the feedback form.\n\n")
        else:
            chat_text.insert(tk.END, f"You: {message}\n\n")
            chat_text.insert(tk.END, "Chatbot: Thank you for contacting us. How can I assist you?\n\n")
        user_input_entry.delete("1.0", tk.END) 
        chatbot_window.lift() 

if __name__ == "__main__":
    root = tk.Tk()
    app = TrafficLightApp(root)
    root.mainloop()
