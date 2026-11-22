from datetime import timedelta
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from .forms import RegisterForm, BookForm, ContactForm
from .models import Book, Category, Loan, Reservation, Favorite, Announcement

def home(request):
    featured = Book.objects.order_by("-created_at")[:6]
    return render(request, "catalog/home.html", {"featured": featured, "categories": Category.objects.all()[:8], "announcements": Announcement.objects.filter(active=True)[:3]})

def register(request):
    if request.user.is_authenticated: return redirect("dashboard")
    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Your account has been created. Welcome!")
        return redirect("dashboard")
    return render(request, "catalog/register.html", {"form": form})

def login_view(request):
    if request.user.is_authenticated: return redirect("dashboard")
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())
        messages.success(request, "You are now logged in.")
        return redirect("dashboard")
    return render(request, "catalog/login.html", {"form": form})

def book_list(request):
    books = Book.objects.select_related("category").all()
    query = request.GET.get("q", "").strip()
    category = request.GET.get("category", "")
    if query: books = books.filter(Q(title__icontains=query) | Q(author__icontains=query) | Q(isbn__icontains=query))
    if category.isdigit(): books = books.filter(category_id=int(category))
    return render(request, "catalog/book_list.html", {"books": books, "categories": Category.objects.all(), "query": query, "selected_category": category})

def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    is_favorite = request.user.is_authenticated and Favorite.objects.filter(member=request.user, book=book).exists()
    return render(request, "catalog/book_detail.html", {"book": book, "is_favorite": is_favorite})

@login_required
def dashboard(request):
    if request.user.is_staff:
        context = {"is_admin": True, "book_count": Book.objects.count(), "member_count": __import__("django.contrib.auth.models", fromlist=["User"]).User.objects.filter(is_staff=False).count(), "active_loans": Loan.objects.filter(status="issued").count(), "overdue_count": Loan.objects.filter(status="issued", due_date__lt=timezone.localdate()).count(), "recent_loans": Loan.objects.select_related("book", "member").order_by("-issued_at")[:8]}
    else:
        context = {"is_admin": False, "loans": Loan.objects.filter(member=request.user).select_related("book").order_by("-issued_at"), "reservations": Reservation.objects.filter(member=request.user).select_related("book")[:5], "favorites": Favorite.objects.filter(member=request.user).select_related("book")[:6]}
    return render(request, "catalog/dashboard.html", context)

@login_required
def favorite_toggle(request, pk):
    if request.method != "POST": return redirect("book_detail", pk=pk)
    book = get_object_or_404(Book, pk=pk)
    fav, created = Favorite.objects.get_or_create(member=request.user, book=book)
    if not created: fav.delete()
    messages.info(request, "Added to favourites." if created else "Removed from favourites.")
    return redirect("book_detail", pk=pk)

@login_required
def reserve_book(request, pk):
    if request.method != "POST": return redirect("book_detail", pk=pk)
    book = get_object_or_404(Book, pk=pk)
    if not Reservation.objects.filter(book=book, member=request.user, status="pending").exists():
        Reservation.objects.create(book=book, member=request.user)
        messages.success(request, "Your reservation request has been submitted.")
    else: messages.info(request, "You already have a pending reservation for this book.")
    return redirect("dashboard")

def contact(request):
    form = ContactForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Thanks! Your message has been received.")
        return redirect("contact")
    return render(request, "catalog/contact.html", {"form": form})

def about(request): return render(request, "catalog/about.html")

def staff_required(view):
    return user_passes_test(lambda u: u.is_authenticated and u.is_staff)(view)

@staff_required
def book_create(request):
    form = BookForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Book added successfully.")
        return redirect("book_list")
    return render(request, "catalog/book_form.html", {"form": form, "heading": "Add a book"})

@staff_required
def book_edit(request, pk):
    book = get_object_or_404(Book, pk=pk)
    form = BookForm(request.POST or None, instance=book)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Book details updated.")
        return redirect("book_detail", pk=pk)
    return render(request, "catalog/book_form.html", {"form": form, "heading": "Edit book"})

@staff_required
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        book.delete()
        messages.success(request, "Book deleted.")
        return redirect("book_list")
    return render(request, "catalog/confirm_delete.html", {"object": book})

@staff_required
def issue_book(request):
    if request.method == "POST":
        book = get_object_or_404(Book, pk=request.POST.get("book_id"))
        from django.contrib.auth.models import User
        member = get_object_or_404(User, pk=request.POST.get("member_id"), is_staff=False)
        if book.available_copies < 1:
            messages.error(request, "No copies are currently available.")
        else:
            Loan.objects.create(book=book, member=member, due_date=timezone.localdate() + timedelta(days=14))
            book.available_copies -= 1
            book.save(update_fields=["available_copies"])
            messages.success(request, f"{book.title} issued to {member.username}.")
        return redirect("dashboard")
    from django.contrib.auth.models import User
    return render(request, "catalog/issue_book.html", {"books": Book.objects.filter(available_copies__gt=0), "members": User.objects.filter(is_staff=False)})

@staff_required
def return_book(request, pk):
    loan = get_object_or_404(Loan, pk=pk, status="issued")
    if request.method == "POST":
        loan.status = "returned"
        loan.returned_at = timezone.now()
        loan.save()
        loan.book.available_copies = min(loan.book.available_copies + 1, loan.book.total_copies)
        loan.book.save(update_fields=["available_copies"])
        messages.success(request, f"Book returned. Fine: ₹{loan.fine}")
        return redirect("dashboard")
    return render(request, "catalog/confirm_return.html", {"loan": loan})
