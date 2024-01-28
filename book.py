
class Book:
    def __init__(self, title, author, publication_year, is_textbook=False):
        self.title = title
        self.author = author
        self.publication_year = publication_year
        self.is_textbook = is_textbook
        self.due_date = None
        self.extension_attempts = 0
