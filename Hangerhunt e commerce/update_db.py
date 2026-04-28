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

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS colors (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(50) NOT NULL,
        hex_code VARCHAR(7) NOT NULL
    );
    """)

    try:
        cursor.execute("""
        ALTER TABLE customer_orders 
        ADD COLUMN color VARCHAR(50);
        """)
    except Exception as e:
        print(f"Column might already exist: {e}")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        fabric VARCHAR(255),
        price DECIMAL(10,2) NOT NULL,
        image_path VARCHAR(255),
        description TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    conn.commit()
    print("DB updated successfully.")
except Exception as e:
    print(f"Error: {e}")
finally:
    if 'cursor' in locals():
        cursor.close()
    if 'conn' in locals() and conn.is_connected():
        conn.close()
