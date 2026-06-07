# 🧥 Hanger Hunt – Full-Stack T-Shirt E-Commerce Platform

Hanger Hunt is a full-stack e-commerce web application that enables customers to browse, purchase, and customize T-shirts through an intuitive online shopping experience. The platform provides dedicated customer and administrator modules for seamless product management, order processing, and customization services.

Built using **Flask**, **MySQL**, **HTML**, **CSS**, and **JavaScript**, the application demonstrates end-to-end e-commerce functionality, including authentication, product management, order tracking, and custom product design uploads.

---

## 🚀 Key Features

### Customer Module

* User registration and authentication using mobile number and password.
* Password recovery through mobile number verification.
* Browse and search T-shirt collections by product name or fabric type.
* View detailed product information, including price, description, fabric type, and available colors.
* Purchase collection products by selecting size, color, and quantity.
* Place custom T-shirt orders by uploading personalized front and back design images.
* Secure checkout process with delivery address management.
* View order history and track previous purchases.
* Persistent login sessions for enhanced user convenience.

### Administrator Module

* Secure administrator authentication.
* Centralized dashboard for platform management.
* Add, update, and remove products from the catalog.
* Manage available T-shirt colors and color codes.
* View and monitor customer orders.
* Filter orders based on dates for efficient order management.
* Automatically generate default administrator credentials during initial setup.

---

## 🛠️ Technology Stack

| Category           | Technologies                       |
| ------------------ | ---------------------------------- |
| Backend            | Python, Flask                      |
| Frontend           | HTML5, CSS3, JavaScript            |
| Database           | MySQL                              |
| Authentication     | Werkzeug Password Hashing          |
| File Handling      | Secure File Uploads using Werkzeug |
| Session Management | Flask Sessions                     |

---

## 📂 Project Structure

```text
Hanger-Hunt/
│
├── app.py
├── database.sql
├── requirements.txt
├── apply_phase2_db.py
├── update_db.py
├── fix_db.py
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── customer_login.html
│   ├── forgot_password.html
│   ├── product.html
│   ├── customize.html
│   ├── address.html
│   ├── profile.html
│   ├── admin_login.html
│   └── admin_dashboard.html
│
└── static/
    ├── css/
    ├── js/
    └── uploads/
        ├── collection/
        └── custom/
```

---

## ⚙️ Installation and Setup

### Prerequisites

* Python 3.8 or above
* MySQL Server
* pip package manager

### Clone the Repository

```bash
git clone https://github.com/NithishKumar38/Hanger-Hunt-T-shirt-E-Commerce-Website-.git
cd Hanger-Hunt-T-shirt-E-Commerce-Website-
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure the Database

Import the provided SQL schema:

```bash
mysql -u root -p < database.sql
```

Update the database configuration in `app.py`:

```python
DB_CONFIG = {
    "host": "localhost",
    "database": "hangerhunt_db",
    "user": "your_username",
    "password": "your_password"
}
```

### Run the Application

```bash
python app.py
```

Open your browser and visit:

```text
http://127.0.0.1:5000
```

---

## 🔑 Default Administrator Credentials

The application automatically creates a default administrator account during the first execution.

| Credential    | Value      |
| ------------- | ---------- |
| Mobile Number | 1234567890 |
| Password      | admin123   |

**Admin Login URL**

```text
http://127.0.0.1:5000/admin/login
```

> For security reasons, it is strongly recommended to change the default credentials before deploying the application.

---

## 📦 Database Design

The application uses the following core tables:

| Table Name      | Description                            |
| --------------- | -------------------------------------- |
| customer_login  | Stores customer account information    |
| admin_login     | Stores administrator credentials       |
| products        | Stores product catalog details         |
| customer_orders | Stores collection and custom orders    |
| colors          | Stores available T-shirt color options |

---

## 🛍️ Order Types

### Collection Orders

Customers can purchase products from the existing catalog by selecting preferred size, color, and quantity.

### Custom Orders

Customers can upload personalized front and back design images and place customized T-shirt orders according to their preferences.

---

## 🔒 Security Features

* Passwords are securely hashed using Werkzeug's password hashing mechanism.
* File uploads are validated and stored using secure file naming practices.
* Restricted administrator routes protected through session-based authentication.
* Image upload validation supporting only approved file formats (`.png`, `.jpg`, `.jpeg`).
* Session management for secure user authentication.

---

## 📈 Future Enhancements

* Online payment gateway integration.
* Email and SMS notifications.
* Product reviews and ratings.
* Order status tracking.
* Inventory management system.
* Responsive mobile-first UI improvements.
* REST API support for mobile applications.

---

## 👨‍💻 Author

**Nithish Kumar M**

GitHub: https://github.com/NithishKumar38

---

## 📄 License

This project is licensed under the MIT License.

---

⭐ If you found this project useful, consider giving the repository a star.
