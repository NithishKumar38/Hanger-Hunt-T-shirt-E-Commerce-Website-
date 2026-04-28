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
        cursor.execute("ALTER TABLE customer_login ADD COLUMN name VARCHAR(255) AFTER id;")
        print("Added 'name' column to customer_login.")
    except Exception as e:
        print(f"Skipping adding 'name' to customer_login (might already exist): {e}")

    try:
        cursor.execute("""
        ALTER TABLE customer_orders
        ADD COLUMN collection_image_path VARCHAR(255) AFTER product_details,
        CHANGE COLUMN front_image_path custom_front_image_path VARCHAR(255),
        CHANGE COLUMN back_image_path custom_back_image_path VARCHAR(255);
        """)
        print("Updated customer_orders table with new image columns.")
    except Exception as e:
        print(f"Skipping customer_orders image columns update (might already be applied): {e}")

    conn.commit()
    print("Database updates completed.")

except Exception as e:
    print(f"Database connection error: {e}")
finally:
    if 'cursor' in locals():
        cursor.close()
    if 'conn' in locals() and conn.is_connected():
        conn.close()
