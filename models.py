from mongoengine import Document, StringField, BooleanField, ListField, ReferenceField, DateTimeField, FloatField, IntField


class User(Document):
    name = StringField(required=True)
    role = StringField(required=True, choices=['Student', 'Faculty', 'Staff', 'Graduate'])
    is_graduate = BooleanField(default=False)
    library_card = StringField()
    hashed_password = StringField(required=True)
    borrowed_books = ListField(ReferenceField('Book'))
    reserved_books = ListField(ReferenceField('Book'))
    fines = FloatField(default=0.0)


class Book(Document):
    title = StringField(required=True)
    author = StringField(required=True)
    isbn = StringField(required=True)
    borrowed = BooleanField(default=False)
    reserved = BooleanField(default=False)
    due_date = DateTimeField()
    reservation_date = DateTimeField()
