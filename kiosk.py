
class Kiosk:
    def __init__(self, las):
        self.las = las

    def search_book(self, title):
        return self.las.search_book(title)

    def reserve_book(self, user, title):
        return self.las.reserve_book(user, title)

    def borrow_book(self, user, title, pin, days=15):
        if user.can_borrow():
            if self.las.validate_pin(user, pin):
                result = self.las.lend_book(user, title, days)
                return f"Borrowing through Kiosk: {result}"
            else:
                return "Invalid PIN code."
        return "Graduates cannot borrow books from Kiosks."

    def extend_due_date(self, user, title, pin, days=15):
        if user.can_borrow():
            if self.las.validate_pin(user, pin):
                result = self.las.extend_due_date(user, title, days)
                return f"Extension via Kiosk: {result}"
            else:
                return "Invalid PIN code."
        return "Graduates cannot extend due dates via Kiosks."

    def send_reservation_email(self, user, title):
        # In a real implementation, you would send an email to the user.
        # For the sake of this example, we print a message.

        print(f"Email notification sent to {user.name}: Your reserved book '{title}' has arrived.")
