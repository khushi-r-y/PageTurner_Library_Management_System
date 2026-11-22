from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("books/", views.book_list, name="book_list"),
    path("books/add/", views.book_create, name="book_create"),
    path("books/<int:pk>/", views.book_detail, name="book_detail"),
    path("books/<int:pk>/edit/", views.book_edit, name="book_edit"),
    path("books/<int:pk>/delete/", views.book_delete, name="book_delete"),
    path("books/<int:pk>/favorite/", views.favorite_toggle, name="favorite_toggle"),
    path("books/<int:pk>/reserve/", views.reserve_book, name="reserve_book"),
    path("issue/", views.issue_book, name="issue_book"),
    path("return/<int:pk>/", views.return_book, name="return_book"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
]
