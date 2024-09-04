import pandas as pd
import mysql.connector

def update_usernames_from_csv(csv_file, database_info):
    try:
        # Connect to MySQL database
        conn = mysql.connector.connect(**database_info)
        cursor = conn.cursor()

        # Read data from CSV file
        df = pd.read_csv(csv_file)

        # Iterate through each row in the DataFrame and update database
        for index, row in df.iterrows():
            reg_no = row['reg_no']
            username = row['username']
            update_query = "UPDATE log_std SET username = %s WHERE reg_no = %s"
            cursor.execute(update_query, (username, reg_no))
            conn.commit()
            print(f"Updated username '{username}' for reg_no '{reg_no}' in database.")

        # Close database connection
        cursor.close()
        conn.close()
        print("Database connection closed.")
    except Exception as e:
        print(f"Error updating usernames from CSV: {e}")

def main():
    csv_file = 'D:\project\sap\\aid.csv'
    
    database_info = {
        'host': 'localhost',
        'user': 'root',
        'password': 'Admin@123',
        'database': 'sap'
    }

    update_usernames_from_csv(csv_file, database_info)

if __name__ == "__main__":
    main()
