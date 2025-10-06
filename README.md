# Online Store

An online store project built with **Django** that allows managing products, categories, users, and orders. The project includes a professional admin panel, product display, shopping cart, SMS-based authentication, and payment gateway integration.

This project is ideal for learning full-stack Django development or as a starting point for a production-level e-commerce platform.

---

## Technologies

- **Backend:** Python, Django  
- **Frontend:** HTML, CSS, JavaScript  
- **Database:** MySQL  
- **APIs:** SMS authentication, ZarinPal payment gateway

---

## Features

- Product management with categories and detailed information  
- User registration and authentication (with SMS verification)  
- Shopping cart and order management  
- Admin panel for managing products, users, and orders  
- Payment gateway integration (ZarinPal)  
- Automatic handling of product images in the `media/` folder

---

## Installation and Setup

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

### 3. Install required packages

```bash
pip install -r requirements.txt
```

### 4. Configure the database

Create a MySQL database and enter the connection details in `settings.py` or a `.env` file:

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

> The application will be accessible at `http://127.0.0.1:8000/`.

---

## Important Notes

- **SMS Authentication and Payment Gateway:** You need to provide your own API keys for SMS verification and ZarinPal payment integration.  
- **Media Folder:** Ensure the `media/` folder exists alongside `static/`. Product images will be automatically saved in an organized structure within this folder.  
- **Sensitive Files:** Files like `venv/` and `.env` are ignored in GitHub for security reasons.

---

## Project Structure

```
shop_project/
│
├── shop/
│   ├── apps/           # Project applications
│   ├── shop/           # Django settings and main files
│   ├── static/         # CSS, JS, and static assets
│   ├── media/          # Product and user images
│   └── templates/      # HTML templates
│
├── venv/               # Virtual environment (ignored by Git)
├── .gitignore
├── manage.py
└── requirements.txt
```

---

## License

This project is for **educational and personal development purposes**. Review security and configuration settings before deploying in a production environment.

---

## Contact / Portfolio

For professional inquiries or collaboration, feel free to contact me:

- **GitHub:** [https://github.com/MohammadSalkhorde](https://github.com/MohammadSalkhorde)  
- **Email:** m.salkhorde444@gmail.com 
- **LinkedIn:** [https://www.linkedin.com/in/mohammad-salkhorde-a13767385](https://www.linkedin.com/in/mohammad-salkhorde-a13767385)
- **Portfolio:** [https://mohammadsalkhorde.github.io/portfolio/](https://mohammadsalkhorde.github.io/portfolio/)
