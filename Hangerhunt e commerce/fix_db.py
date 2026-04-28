import mysql.connector

DB_CONFIG = {
    'host': 'localhost',
    'database': 'hangerhunt_db',
    'user': 'root',
    'password': 'root' 
}

try:
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    try:
        cursor.execute("ALTER TABLE customer_login ADD COLUMN name VARCHAR(255) AFTER id")
        conn.commit()
        print("Successfully added the 'name' column.")
    except mysql.connector.Error as err:
        if err.errno == 1060: # Duplicate column
            print("The 'name' column already exists.")
        else:
            print(f"Error executing ALTER TABLE: {err}")
    finally:
        cursor.close()
        conn.close()
except mysql.connector.Error as e:
    print(f"Database connection error: {e}")
