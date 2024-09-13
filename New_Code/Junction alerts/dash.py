from flask import Flask
import sqlite3

app = Flask(__name__)
db_file = "vehicle_data1.db"

# Function to fetch vehicle data from the database
def fetch_vehicle_data():
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT id, car, lat, lon, speed FROM vehicles")  # Select only required columns
    data = cursor.fetchall()
    conn.close()
    return data

@app.route('/vehicle_dashboard', methods=['GET'])
def vehicle_dashboard():
    try:
        vehicle_data = fetch_vehicle_data()
        if vehicle_data:
            # Render HTML dynamically
            html_content = """
            <html>
            <head><title>Vehicle Dashboard</title></head>
            <body>
            <h1>Vehicle Dashboard</h1>
            <table border='1'>
            <thead>
            <tr>
            <th>ID</th>
            <th>Vehicle</th>
            <th>Latitude</th>
            <th>Longitude</th>
            <th>Speed</th>                     
            </tr>
            </thead>
            <tbody>
            """
            for data in vehicle_data:
                html_content += f"""
                <tr>
                <td>{data[0]}</td>
                <td>{data[1]}</td>
                <td>{data[2]}</td>
                <td>{data[3]}</td>
                <td>{data[4]}</td>
                </tr>
                """
            html_content += """
            </tbody>
            </table>
            </body>
            </html>
            """
            return html_content
        else:
            return "No data available", 404
    except Exception as e:
        return f"An error occurred: {str(e)}", 500

if __name__ == "__main__":
    app.run(debug=True)
