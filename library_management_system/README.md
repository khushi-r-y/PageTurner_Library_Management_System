# PageTurner Library Management System

A ready-to-run Django library website with a public homepage, book catalogue, member registration/login, student dashboard, staff dashboard, book management, issue/return workflow, reservations, favourites, and Django admin.

## Requirements
- Python 3.10 or newer
- Internet connection for Bootstrap, Font Awesome, Google Fonts, and remote Unsplash imagery (the core app works without these assets, but the visual experience is reduced).

## Windows installation (PowerShell)

1. Extract the ZIP.
2. Open PowerShell in the extracted `library_management_system` folder (the folder containing `manage.py`).
3. Create and activate a virtual environment:

```powershell
py -m venv env
env\Scripts\activate
```

4. Install packages:

```powershell
python -m pip install -r requirements.txt
```

5. Create database tables:

```powershell
python manage.py makemigrations catalog
python manage.py migrate
```

6. Create an administrator account:

```powershell
python manage.py createsuperuser
```

7. Start the website:

```powershell
python manage.py runserver
```

8. Open http://127.0.0.1:8000/

## Main URLs
- Website: http://127.0.0.1:8000/
- Book catalogue: http://127.0.0.1:8000/books/
- Register: http://127.0.0.1:8000/register/
- Login: http://127.0.0.1:8000/login/
- Member dashboard: http://127.0.0.1:8000/dashboard/
- Admin panel: http://127.0.0.1:8000/admin/

## First-time setup
1. Log in to `/admin/` using the superuser account.
2. Add categories under **Categories**.
3. Add books under **Books**. Set total copies and available copies to the same number initially.
4. Members can create their own accounts from **Create account**.
5. To make a staff account, use Django Admin > Users and enable **Staff status** for that user.
6. Staff users can add/edit books, issue books, and confirm returns from the website dashboard.

## Notes
- The standard loan period is 14 days.
- The default overdue fine is ₹5 per day. Update `fine_per_day` on a loan in Django Admin if your policy differs.
- Logout uses a POST form for security.
- This is a development starter project. Before public deployment, set a strong `DJANGO_SECRET_KEY`, set `DJANGO_DEBUG=False`, configure production `ALLOWED_HOSTS`, HTTPS, email/password reset, backups, and a production database.
- Book cover images use optional image URLs. Use image URLs you have permission to display.
- The contact page currently saves messages in the database; it does not send email.
