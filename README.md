# Savora — Restaurant Management System

A Django-based restaurant management web application designed to simplify menu browsing, table management, reservations, and order processing through a clean, responsive user interface.

## Features

* **Dashboard:** Overview of menu items, tables, reservations, and orders.
* **Menu Management:** Browse menu items, categories, prices, and stock availability.
* **Table Management:** View restaurant tables, seating capacity, and availability.
* **Reservations:** Create customer reservations with table details.
* **Order Management:** Place orders with multiple menu items and quantities.
* **Inventory Tracking:** Automatically update stock when orders are placed and restore stock when orders are cancelled.
* **Order History:** View previous orders and their current status.
* **Order Status Updates:** Track orders through Pending, In Progress, Completed, and Cancelled states.
* **Responsive UI:** Clean interface designed for desktop and mobile screens.

## Technology Stack

* **Backend:** Python, Django
* **Frontend:** HTML, CSS, JavaScript
* **Database:** SQLite
* **Tools:** VS Code, Git, GitHub

## Project Structure

```text
CodeAlpha_Restaurant_Management_System/
├── manage.py
├── db.sqlite3
├── restaurant_management/
│   ├── settings.py
│   ├── urls.py
│   └── ...
└── restaurant/
    ├── migrations/
    ├── templates/
    │   └── restaurant/
    ├── models.py
    ├── forms.py
    ├── views.py
    ├── urls.py
    └── ...
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd CodeAlpha_Restaurant_Management_System
```

Replace `YOUR_GITHUB_REPOSITORY_URL` with your actual GitHub repository URL.

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install Django

```bash
python -m pip install django
```

If you have a `requirements.txt` file, install all project dependencies instead:

```bash
python -m pip install -r requirements.txt
```

### 4. Apply database migrations

```bash
python manage.py migrate
```

### 5. Create an administrator account (optional)

```bash
python manage.py createsuperuser
```

### 6. Start the development server

```bash
python manage.py runserver
```

Open the application at:

http://127.0.0.1:8000/

Access the Django administration panel at:

http://127.0.0.1:8000/admin/

## Usage

1. Open the dashboard to view restaurant information.
2. Browse menu items and check their availability.
3. View available tables and create reservations.
4. Place orders by selecting a table and menu items.
5. Track orders through the order history page.
6. Update order statuses and verify inventory changes.

## Database

The project uses SQLite for local development. Django migrations manage database schema changes.

## Future Enhancements

* Customer authentication and role-based access.
* Online payment integration.
* Sales reports and analytics.
* Email or SMS reservation confirmations.
* Deployment to a cloud hosting platform.

## Author

**Leelaprasath V.**

Computer Science and Engineering Student

## License

This project was developed for educational and internship purposes.
