from django.contrib import admin
from .models import Category, Book, Loan, Reservation, Favorite, ContactMessage, Announcement

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "category", "available_copies", "total_copies")
    list_filter = ("category",)
    search_fields = ("title", "author", "isbn")

@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ("book", "member", "issued_at", "due_date", "status")
    list_filter = ("status", "due_date")
    search_fields = ("book__title", "member__username")

admin.site.register([Category, Reservation, Favorite, ContactMessage, Announcement])
admin.site.site_header = "Library Administration"
admin.site.site_title = "Library Admin"
admin.site.index_title = "Manage your library"
