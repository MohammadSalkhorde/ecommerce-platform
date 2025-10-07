# 🛍️ ProShop - Professional E-commerce Platform

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![Django](https://img.shields.io/badge/Django-5.0-success?logo=django)
![DRF](https://img.shields.io/badge/DRF-3.15-red?logo=django)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6-yellow?logo=javascript)
![License](https://img.shields.io/badge/License-MIT-yellow)

ProShop is a **fully-featured e-commerce platform** built with **Django** and **Django REST Framework**, offering user registration with SMS authentication, personalized dashboards, and advanced admin features.  
Designed both as a **learning project** and a **foundation for production-level applications**.

---

## 🚀 Key Highlights

- Modular architecture built with Django REST Framework  
- SMS-based authentication (Kavenegar API)  
- Integrated ZarinPal Payment Gateway  
- Full Admin Dashboard for products, orders, and discounts  
- Clean, scalable, and ready for deployment  

---

## 🧠 Technologies

* **Backend:** Python, Django, Django REST Framework  
* **Frontend:** HTML, CSS, JavaScript  
* **Databases:** MySQL, PostgreSQL, SQLite, MongoDB  
* **APIs:** SMS authentication, ZarinPal payment gateway  

---

## ⚙️ Features

### 👤 User Dashboard

* User registration & login with SMS verification  
* Profile management with profile picture  
* Order history, payment records, and invoices  
* Wishlist, compare list, and shopping cart  

### 🛒 Product Management

* Product listing with filtering and categories  
* Admin control over sliders, discounts, and bundles  
* Automatic product discount calculations  
* Advanced search & filtering features  

### 💳 Orders & Payment

* Shopping cart and checkout process  
* Payment via ZarinPal gateway  
* Order tracking and invoice generation  

### 🛠️ Admin Panel

* Manage products, categories, users, and orders  
* Control banners, sliders, and promotional campaigns  
* Create and manage discounts efficiently  

---

## 🧩 Installation & Setup

### 1️⃣ Clone the project

```bash
git clone https://github.com/MohammadSalkhorde/shop_project.git
cd shop_project
```

### 2️⃣ Create and activate a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Configure the database

Set your database credentials in `.env` or `settings.py`:

```
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_HOST=localhost
DB_PORT=3306

ZARINPAL_MERCHANT_ID=your_merchant_id
KAVENEGAR_API_KEY=your_api_key
```

### 5️⃣ Apply migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6️⃣ Run the development server

```bash
python manage.py runserver
```

> Access the application at: http://127.0.0.1:8000/

---

## 📁 Project Structure

```
shop_project/
│
├── shop/
│   ├── apps/
│   ├── middlewares/
│   ├── static/
│   ├── media/
│   └── templates/
│   ├── manage.py
│   ├── utils.py
│   └── custompermissions.py
│
├── venv/
├── .gitignore
├── README.md
├── .env.example
└── requirements.txt
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 💼 Contact & Portfolio

Hi, I'm **Mohammad Salkhorde** 👋  
**Python / Django Backend Developer** — building REST APIs and web applications.  
Open to **freelance** & **remote** opportunities.

* **GitHub:** [https://github.com/MohammadSalkhorde](https://github.com/MohammadSalkhorde)  
* **LinkedIn:** [https://www.linkedin.com/in/mohammad-salkhorde-a13767385](https://www.linkedin.com/in/mohammad-salkhorde-a13767385)  
* **Portfolio:** [https://mohammadsalkhorde.github.io/portfolio/](https://mohammadsalkhorde.github.io/portfolio/)  
* **Email:** [m.salkhorde444@gmail.com](mailto:m.salkhorde444@gmail.com)
