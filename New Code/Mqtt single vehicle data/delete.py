import sqlite3

def delete_vehicle_data(database_file):
    try:
        # Connect to the database
        conn = sqlite3.connect(database_file)
        cursor = conn.cursor()

        # Execute SQL command to delete all data from the table
        cursor.execute("DELETE FROM vehicle_parameters")
        
        # Commit the transaction
        conn.commit()
        print("All data deleted successfully.")
        
    except sqlite3.Error as e:
        print("Error occurred:", e)
        
    finally:
        # Close the connection
        if conn:
            conn.close()

# Provide the path to your database file
database_file = "data.db"

# Call the function to delete data
delete_vehicle_data(database_file)
