# PageTurner – Library Management System

PageTurner is a web-based Library Management System developed using Python and Django. It provides an easy-to-use platform for managing books, members, reservations, and book circulation.

**Live Website:** https://khushiry.pythonanywhere.com/

## Features

- User Registration and Login
- User Logout
- Member Dashboard
- Staff Dashboard
- Book Catalogue
- Search and Filter Books
- Book Details
- Book Cover Images
- Add Books
- Edit Books
- Delete Books
- Add Books to Favourites
- Book Reservations
- Issue and Return Books
- 14-Day Loan Period
- Overdue Fine Calculation (₹5 per day)
- Django Admin Panel

## Technologies Used

- Python
- Django
- HTML
- CSS
- JavaScript
- SQLite Database
- PythonAnywhere Hosting

## Project Structure

```text
PageTurner_Library_Management_System/
│
├── catalog/
├── library_site/
├── templates/
├── static/
├── manage.py
├── requirements.txt
├── db.sqlite3
└── README.md
```

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
```

### 2. Navigate to the Project Folder

```bash
cd PageTurner_Library_Management_System
```

### 3. Create a Virtual Environment

```bash
python -m venv env
```

### 4. Activate the Virtual Environment

**Windows:**

```bash
env\Scripts\activate
```

**Mac/Linux:**

```bash
source env/bin/activate
```

### 5. Install Required Packages

```bash
pip install -r requirements.txt
```

### 6. Apply Database Migrations

```bash
python manage.py migrate
```

### 7. Create an Admin Account

```bash
python manage.py createsuperuser
```

### 8. Run the Development Server

```bash
python manage.py runserver
```

Open your browser and visit:

http://127.0.0.1:8000/

## Admin Panel

Access the Django administration panel:

http://127.0.0.1:8000/admin/

Login using your superuser credentials.

## Live Deployment

The PageTurner Library Management System is deployed using PythonAnywhere.

**Live Website:** https://khushiry.pythonanywhere.com/

## Future Enhancements

- Email Notifications
- Improved User Interface
- Advanced Book Search
- Library Reports
- Enhanced Security
- Additional Library Management Features

## Author

**Project Name:** PageTurner – Library Management System

**Developed using:** Python and Django

---

*PageTurner – Making Library Management Simple and Efficient!*
