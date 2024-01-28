from models import User, Book

from datetime import datetime, timedelta

class LibraryAutomationSystem:
    def add_book(self, title, author, publication_year, is_textbook=False):
        book = Book(title=title, author=author, publication_year=publication_year, is_textbook=is_textbook)
        book.save()

    def search_book(self, title):
        return list(Book.objects(title__icontains=title))

    def add_user(self, name, user_type, is_graduate=False):
        new_user = User(name=name, user_type=user_type, is_graduate=is_graduate)
        new_user.save()
        return new_user

    def lend_book(self, user_id, title, days=15):
        user = User.objects(id=user_id).first()
        book = Book.objects(title=title, borrowed=False).first()
        if user and book and len(user.borrowed_books) < self.get_max_books_borrowed(user):
            book.borrowed = True
            book.due_date = datetime.utcnow() + timedelta(days=days)
            book.save()
            user.update(push__borrowed_books=book)
            return f"Lent book: {title} for {days} days."
        return "Cannot lend book."

    def get_max_books_borrowed(self, user):
        if user.user_type == "Faculty":
            return 5
        return 3

    def reserve_book(self, user_id, title):
        user = User.objects(id=user_id).first()
        book = Book.objects(title=title, borrowed=False, reserved=False).first()
        if user and book:
            if user.user_type == "Faculty" or not book.is_textbook:
                book.update(set__reserved=True)
                user.update(push__reserved_books=book)
                return f"Book reserved: {title}"
            else:
                return "Faculty members can reserve textbooks only."
        return "Book not available for reservation."

    def extend_due_date(self, user_id, title, days=15):
        user = User.objects(id=user_id).first()
        book = Book.objects(title=title, borrowed=True).first()
        if user and book in user.borrowed_books:
            if book.due_date and datetime.utcnow() < book.due_date + timedelta(days=days):
                book.update(inc__due_date=timedelta(days=days))
                return f"Extended due date for {title} by {days} days."
            else:
                return "Cannot extend due date."
        return "Book not found or extension not possible."

    def calculate_fine(self, book):
        if book.due_date and datetime.utcnow() > book.due_date:
            overdue_days = (datetime.utcnow() - book.due_date).days
            if overdue_days <= 7:
                return 10  # Fine for the first week of overdue
            else:
                return 10 + (overdue_days - 1) // 7 * 20  # Subsequent weeks fine
        return 0  # No fine if returned on or before the due date

    def check_reserved_books(self):
        for book in Book.objects(reserved=True):
            if datetime.utcnow() - book.reservation_date >= timedelta(days=2):
                book.update(set__reserved=False)

