from random import choices
import string


class User:
    def __init__(self, name, user_type, is_graduate=False):
        self.name = name
        self.user_type = user_type  # "Student," "Faculty," or "Staff"
        self.is_graduate = is_graduate
        self.library_card = None
        self.borrowed_books = []

        if is_graduate:
            self.library_card = self.SmartCard()
            self.library_card.activate_membership()

    def can_borrow(self):
        if self.user_type == "Graduate" and not self.library_card.is_valid_membership():
            return False
        return len(self.borrowed_books) < self.get_max_books_borrowed()

    def get_max_books_borrowed(self):
        if self.user_type == "Faculty":
            return 5
        return 3

    def get_max_borrowing_days(self):
        if self.user_type == "Faculty":
            return 30
        return 15

    class SmartCard:
        def __init__(self):
            self.membership_valid = False
            self.pin = None

        def activate_membership(self):
            self.membership_valid = True
            self.pin = ''.join(choices(string.digits, k=4))  # Generate a PIN

        def is_valid_membership(self):
            return self.membership_valid
