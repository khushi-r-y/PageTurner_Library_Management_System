from django.core.management.base import BaseCommand
from catalog.models import Book, Category

BOOKS = [
    {
        "title": "Harry Potter and the Philosopher's Stone", "author": "J. K. Rowling",
        "isbn": "9780747532699", "category": "Fantasy",
        "description": "The first adventure of Harry Potter, a young wizard who discovers a remarkable world of magic.",
        "publisher": "Bloomsbury", "published_year": 1997,
    },
    {
        "title": "The Alchemist", "author": "Paulo Coelho",
        "isbn": "9780061122415", "category": "Fiction",
        "description": "A shepherd travels in search of treasure and learns to listen to his heart.",
        "publisher": "HarperOne", "published_year": 1988,
    },
    {
        "title": "Wings of Fire", "author": "A. P. J. Abdul Kalam with Arun Tiwari",
        "isbn": "9788173711466", "category": "Biography",
        "description": "The autobiography of A. P. J. Abdul Kalam, tracing his journey from childhood to public service.",
        "publisher": "Universities Press", "published_year": 1999,
    },
    {
        "title": "Pride and Prejudice", "author": "Jane Austen",
        "isbn": "9780141439518", "category": "Classic Literature",
        "description": "A classic novel about family, first impressions, love, and social expectations.",
        "publisher": "Penguin Classics", "published_year": 1813,
    },
    {
        "title": "The Hobbit", "author": "J. R. R. Tolkien",
        "isbn": "9780547928227", "category": "Fantasy",
        "description": "Bilbo Baggins is drawn into an unexpected journey with a company of dwarves.",
        "publisher": "Houghton Mifflin Harcourt", "published_year": 1937,
    },
    {
        "title": "To Kill a Mockingbird", "author": "Harper Lee",
        "isbn": "9780060935467", "category": "Classic Literature",
        "description": "A novel about justice, empathy, and childhood in the American South.",
        "publisher": "Harper Perennial", "published_year": 1960,
    },
    {
        "title": "The Diary of a Young Girl", "author": "Anne Frank",
        "isbn": "9780553296983", "category": "Biography",
        "description": "The diary of Anne Frank, written while she and her family hid during World War II.",
        "publisher": "Bantam", "published_year": 1947,
    },
    {
        "title": "Atomic Habits", "author": "James Clear",
        "isbn": "9780735211292", "category": "Self-Help",
        "description": "A practical guide to building good habits and making small changes that add up.",
        "publisher": "Avery", "published_year": 2018,
    },
    {
        "title": "The Great Gatsby", "author": "F. Scott Fitzgerald",
        "isbn": "9780743273565", "category": "Classic Literature",
        "description": "A story of ambition, wealth, and the American Dream in the Jazz Age.",
        "publisher": "Scribner", "published_year": 1925,
    },
    {
        "title": "Ikigai", "author": "Héctor García and Francesc Miralles",
        "isbn": "9780143130727", "category": "Self-Help",
        "description": "An exploration of the Japanese concept of finding purpose and meaning in everyday life.",
        "publisher": "Penguin Life", "published_year": 2016,
    },
]

class Command(BaseCommand):
    help = "Add a starter collection of sample books with online cover images."

    def handle(self, *args, **options):
        created_count = 0
        for item in BOOKS:
            category, _ = Category.objects.get_or_create(name=item["category"])
            cover_url = f"https://covers.openlibrary.org/b/isbn/{item['isbn']}-L.jpg?default=false"
            _, created = Book.objects.update_or_create(
                isbn=item["isbn"],
                defaults={
                    "title": item["title"], "author": item["author"],
                    "category": category, "description": item["description"],
                    "cover_url": cover_url, "publisher": item["publisher"],
                    "published_year": item["published_year"],
                    "total_copies": 5, "available_copies": 5,
                },
            )
            if created:
                created_count += 1
        self.stdout.write(self.style.SUCCESS(
            f"Sample collection ready: {len(BOOKS)} books checked; {created_count} newly added."
        ))
