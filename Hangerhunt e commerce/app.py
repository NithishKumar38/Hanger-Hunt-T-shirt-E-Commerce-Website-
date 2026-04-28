from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
from mysql.connector import Error
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
import json
from datetime import timedelta

app = Flask(__name__)
app.secret_key = 'hangerhunt_super_secret_key' # Change in production
app.permanent_session_lifetime = timedelta(days=30) # Persist session for 30 days

# --- Configuration ---
# MySQL Database configuration. Please ensure MySQL Workbench is running locally
DB_CONFIG = {
    'host': 'localhost',
    'database': 'hangerhunt_db',
    'user': 'root', # Replace with your MySQL username
    'password': 'root'  # Replace with your MySQL password
}

# Upload Folders
UPLOAD_FOLDER_COLLECTION = 'static/uploads/collection'
UPLOAD_FOLDER_CUSTOM = 'static/uploads/custom'
os.makedirs(UPLOAD_FOLDER_COLLECTION, exist_ok=True)
os.makedirs(UPLOAD_FOLDER_CUSTOM, exist_ok=True)
app.config['UPLOAD_FOLDER_COLLECTION'] = UPLOAD_FOLDER_COLLECTION
app.config['UPLOAD_FOLDER_CUSTOM'] = UPLOAD_FOLDER_CUSTOM

# Allowed extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# --- Database Helper ---
def get_db_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        if conn.is_connected():
            return conn
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

# --- Routes ---

@app.route('/')
def index():
    # Fetch collections from database to display on homepage
    conn = get_db_connection()
    products = []
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM products ORDER BY created_at DESC")
        products = cursor.fetchall()
        cursor.close()
        conn.close()
    return render_template('index.html', products=products)

# --- Customer Authentication ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form.get('name') # Added for Phase 2
        mobile = request.form.get('mobile_number')
        password = request.form.get('password')
        action = request.form.get('action') # 'login' or 'register'
        
        conn = get_db_connection()
        if not conn:
             flash("Database connection error.", "danger")
             return render_template('customer_login.html')

        cursor = conn.cursor(dictionary=True)
        
        if action == 'register':
            # Simplified registration flow during login page for ease of use
            cursor.execute("SELECT * FROM customer_login WHERE mobile_number = %s", (mobile,))
            if cursor.fetchone():
                flash("Mobile number already registered.", "danger")
            else:
                hashed_pw = generate_password_hash(password)
                cursor.execute("INSERT INTO customer_login (name, mobile_number, password) VALUES (%s, %s, %s)", (name, mobile, hashed_pw))
                conn.commit()
                flash("Registration successful. You can now login.", "success")
        else:
            # Login flow
            cursor.execute("SELECT * FROM customer_login WHERE mobile_number = %s", (mobile,))
            user = cursor.fetchone()
            if user and check_password_hash(user['password'], password):
                session.permanent = True # Ensure persistent login
                session['customer_mobile'] = user['mobile_number']
                session['customer_name'] = user.get('name', 'Customer') # Store name
                return redirect(url_for('index'))
            else:
                flash("Invalid mobile number or password.", "danger")
                
        cursor.close()
        conn.close()

    return render_template('customer_login.html')

@app.route('/logout')
def logout():
    session.pop('customer_mobile', None)
    session.pop('customer_name', None)
    return redirect(url_for('index'))

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        mobile = request.form.get('mobile_number')
        new_password = request.form.get('new_password')
        
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            # In a real app, verify OTP here. We are doing direct password assignment for the assignment's simplicity.
            hashed_pw = generate_password_hash(new_password)
            cursor.execute("UPDATE customer_login SET password = %s WHERE mobile_number = %s", (hashed_pw, mobile))
            if cursor.rowcount > 0:
                conn.commit()
                flash("Password updated successfully.", "success")
                return redirect(url_for('login'))
            else:
                flash("Mobile number not found.", "danger")
            cursor.close()
            conn.close()
    return render_template('forgot_password.html')


# --- Admin Authentication & Dashboard ---
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        mobile = request.form.get('mobile_number')
        password = request.form.get('password')
        
        # Hardcoded setup of initial admin if none exists (for ease of use locally)
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM admin_login")
            if not cursor.fetchone():
               default_hash = generate_password_hash('admin123')
               cursor.execute("INSERT INTO admin_login (mobile_number, password) VALUES (%s, %s)", ('1234567890', default_hash))
               conn.commit()
            
            cursor.execute("SELECT * FROM admin_login WHERE mobile_number = %s", (mobile,))
            admin = cursor.fetchone()
            if admin and check_password_hash(admin['password'], password):
                session['admin_mobile'] = admin['mobile_number']
                return redirect(url_for('admin_dashboard'))
            else:
                flash("Invalid admin credentials.", "danger")
            cursor.close()
            conn.close()
    return render_template('admin_login.html')

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_mobile', None)
    return redirect(url_for('admin_login'))

@app.route('/admin/dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    if 'admin_mobile' not in session:
        return redirect(url_for('admin_login'))
        
    conn = get_db_connection()
    if request.method == 'POST':
        # Admin uploading new product to collection
        name = request.form.get('name')
        fabric = request.form.get('fabric')
        price = request.form.get('price')
        description = request.form.get('description', '')
        image = request.files.get('image')
        
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER_COLLECTION'], filename)
            image.save(filepath)
            
            # Save to DB
            cursor = conn.cursor()
            img_db_path = f"uploads/collection/{filename}"
            cursor.execute("INSERT INTO products (name, fabric, price, image_path, description) VALUES (%s, %s, %s, %s, %s)", 
                           (name, fabric, price, img_db_path, description))
            conn.commit()
            cursor.close()
            flash("New product added to collection!", "success")
            
    date_filter = request.args.get('date', '')
    orders = []
    products = []
    colors = []
    
    if conn:
        cursor = conn.cursor(dictionary=True)
        # Fetch Orders with Date Filter
        if date_filter:
            cursor.execute("""
                SELECT co.*, cl.name as customer_name,
                       JSON_UNQUOTE(JSON_EXTRACT(co.product_details, '$.size')) AS size,
                       JSON_UNQUOTE(JSON_EXTRACT(co.product_details, '$.quantity')) AS quantity
                FROM customer_orders co
                LEFT JOIN customer_login cl ON co.customer_mobile = cl.mobile_number
                WHERE co.created_at LIKE %s 
                ORDER BY co.created_at DESC
            """, (f"{date_filter}%",))
        else:
            cursor.execute("""
                SELECT co.*, cl.name as customer_name,
                       JSON_UNQUOTE(JSON_EXTRACT(co.product_details, '$.size')) AS size,
                       JSON_UNQUOTE(JSON_EXTRACT(co.product_details, '$.quantity')) AS quantity
                FROM customer_orders co
                LEFT JOIN customer_login cl ON co.customer_mobile = cl.mobile_number
                ORDER BY co.created_at DESC
            """)
        orders = cursor.fetchall()
        
        # Fetch Products to allow removal
        cursor.execute("SELECT * FROM products ORDER BY created_at DESC")
        products = cursor.fetchall()
        
        # Fetch Colors for management
        cursor.execute("SELECT * FROM colors ORDER BY name")
        colors = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
    return render_template('admin_dashboard.html', orders=orders, products=products, colors=colors, date_filter=date_filter)


# ---------------------------------------------------------
# NEW: Remove Product Route
# ---------------------------------------------------------
@app.route('/admin/products/delete/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    if 'admin_mobile' not in session:
        return redirect(url_for('admin_login'))
    
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM products WHERE id = %s", (product_id,))
        conn.commit()
        cursor.close()
        conn.close()
        flash("Product removed successfully.", "success")
    return redirect(url_for('admin_dashboard'))


# ---------------------------------------------------------
# NEW: Manage Colors Route (Add/Delete actions)
# ---------------------------------------------------------
@app.route('/admin/colors/manage', methods=['POST'])
def manage_colors():
    if 'admin_mobile' not in session:
        return redirect(url_for('admin_login'))
    
    action = request.form.get('action')
    conn = get_db_connection()
    
    if conn:
        cursor = conn.cursor()
        if action == 'add':
            name = request.form.get('name')
            hex_code = request.form.get('hex_code')
            cursor.execute("INSERT INTO colors (name, hex_code) VALUES (%s, %s)", (name, hex_code))
            flash("Color added successfully.", "success")
        elif action == 'delete':
            color_id = request.form.get('color_id')
            cursor.execute("DELETE FROM colors WHERE id = %s", (color_id,))
            flash("Color removed successfully.", "success")
        
        conn.commit()
        cursor.close()
        conn.close()
        
    return redirect(url_for('admin_dashboard'))


# --- Phase 2: Search & Profile ---
@app.route('/search')
def search():
    query = request.args.get('q', '')
    products = []
    if query:
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor(dictionary=True)
            search_pattern = f"%{query}%"
            # Search by name or fabric
            cursor.execute("SELECT * FROM products WHERE name LIKE %s OR fabric LIKE %s ORDER BY created_at DESC", (search_pattern, search_pattern))
            products = cursor.fetchall()
            cursor.close()
            conn.close()
    return render_template('index.html', products=products, search_query=query)

@app.route('/profile')
def profile():
    if 'customer_mobile' not in session:
        return redirect(url_for('login'))
        
    mobile = session['customer_mobile']
    # Start with session name, but query DB for truth
    name = session.get('customer_name', 'Customer')
    
    conn = get_db_connection()
    orders = []
    if conn:
        cursor = conn.cursor(dictionary=True)
        
        # 1. Fetch Dynamic Name from Database
        cursor.execute("SELECT name FROM customer_login WHERE mobile_number = %s", (mobile,))
        user_record = cursor.fetchone()
        if user_record and user_record.get('name'):
            name = user_record['name']
            session['customer_name'] = name # Update session just in case
            
        # 2. Fetch Orders
        cursor.execute("SELECT * FROM customer_orders WHERE customer_mobile = %s ORDER BY created_at DESC", (mobile,))
        orders = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
    return render_template('profile.html', orders=orders, name=name)


# --- Shopping Flows ---
@app.route('/product/<int:product_id>')
def product(product_id):
    conn = get_db_connection()
    product_item = None
    colors = []
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
        product_item = cursor.fetchone()
        
        cursor.execute("SELECT * FROM colors ORDER BY name")
        colors = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
    if product_item:
        return render_template('product.html', product=product_item, colors=colors)
    return "Product not found", 404

@app.route('/customize', methods=['GET', 'POST'])
def customize():
    if request.method == 'POST':
        size = request.form.get('size')
        quantity = request.form.get('quantity')
        color = request.form.get('color')
        front_image = request.files.get('front_image')
        back_image = request.files.get('back_image')
        
        front_path = ""
        back_path = ""
        
        if front_image and allowed_file(front_image.filename):
            fname = secure_filename(front_image.filename)
            front_image.save(os.path.join(app.config['UPLOAD_FOLDER_CUSTOM'], fname))
            front_path = f"uploads/custom/{fname}"
            
        if back_image and allowed_file(back_image.filename):
            bname = secure_filename(back_image.filename)
            back_image.save(os.path.join(app.config['UPLOAD_FOLDER_CUSTOM'], bname))
            back_path = f"uploads/custom/{bname}"
            
        # Store intermediate data in session before address page
        session['order_pending'] = {
            'order_type': 'Custom',
            'details': json.dumps({'size': size, 'quantity': quantity, 'color': color}),
            'collection_img': '',
            'front_img': front_path,
            'back_img': back_path
        }
        return redirect(url_for('address'))

    conn = get_db_connection()
    colors = []
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM colors ORDER BY name")
        colors = cursor.fetchall()
        cursor.close()
        conn.close()

    return render_template('customize.html', colors=colors)

@app.route('/buy_collection/<int:product_id>', methods=['POST'])
def buy_collection(product_id):
    # Route hit when user clicks Buy Now on Product page
    size = request.form.get('size')
    quantity = request.form.get('quantity')
    color = request.form.get('color')
    
    # Fetch the image path for this collection product
    conn = get_db_connection()
    collection_image = ""
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT image_path FROM products WHERE id = %s", (product_id,))
        product = cursor.fetchone()
        if product:
             collection_image = product['image_path']
        cursor.close()
        conn.close()
    
    session['order_pending'] = {
        'order_type': 'Collection',
        'details': json.dumps({'product_id': product_id, 'size': size, 'quantity': quantity, 'color': color}),
        'collection_img': collection_image,
        'front_img': '',
        'back_img': ''
    }
    return redirect(url_for('address'))

@app.route('/address', methods=['GET', 'POST'])
def address():
    if 'order_pending' not in session:
        return redirect(url_for('index'))
        
    if request.method == 'POST':
        name = request.form.get('name')
        mobile = request.form.get('mobile')
        address_text = request.form.get('address')
        pincode = request.form.get('pincode')
        
        # In a real app we might require user login first. For now, we take from form or session
        customer_mobile = session.get('customer_mobile', mobile) 
        
        order_data = session['order_pending']
        
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            details_dict = json.loads(order_data['details'])
            selected_color = details_dict.get('color', '')
            
            cursor.execute("""
                INSERT INTO customer_orders 
                (customer_mobile, order_type, product_details, collection_image_path, custom_front_image_path, custom_back_image_path, address_name, address_mobile, address_text, pincode, color)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (customer_mobile, order_data['order_type'], order_data['details'], 
                  order_data.get('collection_img', ''), order_data.get('front_img', ''), order_data.get('back_img', ''), 
                  name, mobile, address_text, pincode, selected_color))
            conn.commit()
            cursor.close()
            conn.close()
            
            # Clear pending order
            session.pop('order_pending', None)
            return render_template('address.html', success=True)
            
    return render_template('address.html', success=False)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
