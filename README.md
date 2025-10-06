# ProShop - Professional E-commerce Platform

ProShop is a fully-featured online store built with **Django**, offering user registration with SMS authentication, personalized user dashboards, product management, and advanced admin functionalities. The platform is designed for learning full-stack development or as a starting point for production-level e-commerce.

![ProShop Demo](media/demo/homepage.png)

---

## Technologies

* **Backend:** Python, Django, Django REST Framework
* **Frontend:** HTML, CSS, JavaScript
* **Databases:** MySQL, PostgreSQL, SQLite, MongoDB
* **APIs:** SMS authentication, ZarinPal payment gateway

---

## Features

### User Dashboard

* User registration and authentication with SMS verification
* Profile management including profile picture
* Recent orders, payment history, invoices
* Wishlist, compare list, shopping cart

### Product Management

* Product listing with filters and categories
* Admin panel for managing sliders, discounts, and discount bundles
* Automatic application of product discounts
* Advanced product search and filtering

### Orders & Payment

* Shopping cart and checkout process
* Payment via ZarinPal gateway
* Order tracking and invoice generation

### Admin Panel

* Full control over products, categories, users, orders, and discounts
* Slider and banner management
* Discount and promotional campaign management

---

## Installation & Setup

### 1. Clone the project

```bash
git clone https://github.com/MohammadSalkhorde/shop_project.git
cd shop_project
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the database

Set your database credentials in `.env` or `settings.py`:

```
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_HOST=localhost
DB_PORT=3306
```

### 5. Apply migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Run the development server

```bash
python manage.py runserver
```

> Access the application at `http://127.0.0.1:8000/`

---

## Project Structure

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
└── requirements.txt
```

---

## Contact & Portfolio

Hi, I'm Mohammad 👋
Python / Django Backend Developer — building REST APIs and web applications.
Open to freelance & remote opportunities.

* **GitHub:** [https://github.com/MohammadSalkhorde](https://github.com/MohammadSalkhorde)
* **LinkedIn:** [https://www.linkedin.com/in/mohammad-salkhorde-a13767385](https://www.linkedin.com/in/mohammad-salkhorde-a13767385)
* **Portfolio:** [https://MohammadSalkhorde.github.io/portfolio/](https://MohammadSalkhorde.github.io/portfolio/)
* **Email:** [m.salkhorde444@gmail.com](mailto:m.salkhorde444@gmail.com)
