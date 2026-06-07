# 🧥 Hanger Hunt – T-Shirt E-Commerce Platform

Hanger Hunt is a full-stack e-commerce web application that enables customers to browse, purchase, and customize T-shirts through an intuitive online shopping experience. The platform provides dedicated customer and administrator modules for seamless product management, order processing, and customization services.

Built using **Flask**, **MySQL**, **HTML**, **CSS**, and **JavaScript**, the application demonstrates end-to-end e-commerce functionality, including authentication, product management, order tracking, and custom product design uploads.

---

<img width="1920" height="1080" alt="Screenshot (99)" src="https://github.com/user-attachments/assets/662fb582-bc08-4e6d-aca8-b3e7f181f5dd" />

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

<img width="1920" height="1080" alt="Screenshot (101)" src="https://github.com/user-attachments/assets/7e0932ea-cb43-4f11-a8fc-70cd013ff2fd" />


### Administrator Module

* Secure administrator authentication.
* Centralized dashboard for platform management.
* Add, update, and remove products from the catalog.
* Manage available T-shirt colors and color codes.
* View and monitor customer orders.
* Filter orders based on dates for efficient order management.
* Automatically generate default administrator credentials during initial setup.

---
<img width="1920" height="1080" alt="Screenshot (102)" src="https://github.com/user-attachments/assets/47c21ea6-2236-4088-9429-c4480b6c8f4e" />

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

https://github.com/user-attachments/assets/41c5779a-b657-4a7b-b6e8-e006e5e19614



### Custom Orders

Customers can upload personalized front and back design images and place customized T-shirt orders according to their preferences.


https://github.com/user-attachments/assets/3fd8803b-7579-4a90-8bcd-fe67116e4201







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



⭐ If you found this project useful, consider giving the repository a star.
