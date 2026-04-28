-- Create Database
CREATE DATABASE IF NOT EXISTS hangerhunt_db;
USE hangerhunt_db;

-- Customer Login Table
CREATE TABLE IF NOT EXISTS customer_login (
    id INT AUTO_INCREMENT PRIMARY KEY,
    mobile_number VARCHAR(15) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Admin Login Table
CREATE TABLE IF NOT EXISTS admin_login (
    id INT AUTO_INCREMENT PRIMARY KEY,
    mobile_number VARCHAR(15) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Products/Collections Table (Managed by Admin)
CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    fabric VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    image_path VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Customer Orders Table
CREATE TABLE IF NOT EXISTS customer_orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_mobile VARCHAR(15) NOT NULL,
    order_type ENUM('Collection', 'Custom') NOT NULL,
    product_details JSON,  -- Will store size, quantity, or specific product info
    front_image_path VARCHAR(255), -- For custom orders
    back_image_path VARCHAR(255),  -- For custom orders
    address_name VARCHAR(255) NOT NULL,
    address_mobile VARCHAR(15) NOT NULL,
    address_text TEXT NOT NULL,
    pincode VARCHAR(10) NOT NULL,
    status ENUM('Pending', 'Processing', 'Shipped', 'Delivered', 'Cancelled') DEFAULT 'Pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert a default Admin user (Password should be hashed in a real app, storing plain for now just to allow initial login, but the app should handle hashing. We'll use werkzeug to hash 'admin123' -> 'scrypt:32768:8:1$WzK...' in Python later. For now, inserting a dummy hash.)
-- Let's leave insert for python script or just insert a very basic one if needed, but Python app run should create default admin.

-- -------------------------------------------------------------
-- PHASE 2 UPGRADES:
-- Run the following ALTER TABLE command in MySQL Workbench to update 
-- your existing database without dropping it:
-- 
-- ALTER TABLE customer_login ADD COLUMN name VARCHAR(255) AFTER id;
-- -------------------------------------------------------------

-- ALTER TABLE for customer_orders images
-- ALTER TABLE customer_orders
-- ADD COLUMN collection_image_path VARCHAR(255) AFTER product_details,
-- CHANGE COLUMN front_image_path custom_front_image_path VARCHAR(255),
-- CHANGE COLUMN back_image_path custom_back_image_path VARCHAR(255);
