from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    def __str__(self): return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=150)
    isbn = models.CharField(max_length=20, unique=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="books")
    description = models.TextField(blank=True)
    cover_url = models.URLField(blank=True, help_text="Optional image URL for the book cover")
    publisher = models.CharField(max_length=150, blank=True)
    published_year = models.PositiveIntegerField(null=True, blank=True)
    total_copies = models.PositiveIntegerField(default=1)
    available_copies = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return f"{self.title} — {self.author}"
    @property
    def is_available(self): return self.available_copies > 0

class Loan(models.Model):
    STATUS_CHOICES = [("issued", "Issued"), ("returned", "Returned")]
    book = models.ForeignKey(Book, on_delete=models.PROTECT, related_name="loans")
    member = models.ForeignKey(User, on_delete=models.CASCADE, related_name="library_loans")
    issued_at = models.DateTimeField(default=timezone.now)
    due_date = models.DateField()
    returned_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="issued")
    fine_per_day = models.DecimalField(max_digits=7, decimal_places=2, default=5)
    @property
    def overdue_days(self):
        end = self.returned_at.date() if self.returned_at else timezone.localdate()
        return max((end - self.due_date).days, 0)
    @property
    def fine(self): return self.overdue_days * self.fine_per_day
    def __str__(self): return f"{self.book.title} → {self.member.username}"

class Reservation(models.Model):
    STATUS_CHOICES = [("pending", "Pending"), ("fulfilled", "Fulfilled"), ("cancelled", "Cancelled")]
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="reservations")
    member = models.ForeignKey(User, on_delete=models.CASCADE, related_name="library_reservations")
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default="pending")
    class Meta: ordering = ["-created_at"]
    def __str__(self): return f"{self.book.title} reserved by {self.member.username}"

class Favorite(models.Model):
    member = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favorite_books")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="favorited_by")
    class Meta: unique_together = ("member", "book")
    def __str__(self): return f"{self.member.username}: {self.book.title}"

class ContactMessage(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    subject = models.CharField(max_length=180)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.subject

class Announcement(models.Model):
    title = models.CharField(max_length=180)
    message = models.TextField()
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.title
