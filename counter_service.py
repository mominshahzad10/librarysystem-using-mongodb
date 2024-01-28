import time
class CounterService:
    def __init__(self, las):
        self.las = las

    def borrow_book(self, user, title, days=15):
        current_time = time.time()
        if not user.can_borrow():
            return "Borrowing limit reached at the counter."

        max_borrowing_days = user.get_max_borrowing_days()
        for book in self.las.books:
            if book.title == title and (not book.is_textbook or user.user_type == "Faculty"):
                if days <= max_borrowing_days:
                    user.books_borrowed.append(book)
                    # Set the due date for the book
                    book.due_date = current_time + days * 24 * 3600
                    return f"Book borrowed from counter: {title} for {days} days."
                else:
                    return f"Cannot borrow for more than {max_borrowing_days} days from the counter."
            else:
                return "Book not available for borrowing or already reserved at the counter."
