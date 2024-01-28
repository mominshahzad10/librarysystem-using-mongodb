import datetime
import bcrypt
from flask import jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app import producer, users_collection, books_collection, app
from book import Book
from library_automation_system import LibraryAutomationSystem
from models import User, Book
# from user import User
from functools import wraps

las = LibraryAutomationSystem()


def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def verify_password(provided_password, stored_password):
    return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password)


def validate_user(username, password):
    user = users_collection.find_one({"username": username})
    if user and verify_password(password, user['password']):
        return user
    else:
        return None


def role_required(*roles):
    def wrapper(fn):
        @wraps(fn)
        @jwt_required()
        def decorator(*args, **kwargs):
            current_user = get_jwt_identity()
            if current_user['role'] not in roles:
                return jsonify({'message': 'Access denied'}), 403
            return fn(*args, **kwargs)

        return decorator

    return wrapper


@app.route('/create_user', methods=['POST'])
def create_user():
    data = request.json
    hashed_password = hash_password(data['password'])
    new_user = User(
        name=data['name'],
        role=data['role'],
        is_graduate=data.get('is_graduate', False),
        hashed_password=hashed_password
    )
    new_user.save()  # Saves the new user to MongoDB
    return jsonify({'message': 'User created successfully'}), 201


@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    user = validate_user(username, password)
    if user:
        access_token = create_access_token(identity={'username': username, 'role': user['role']})
        return jsonify(access_token=access_token, user={"username": user['username'], "role": user['role']}), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401


# Book Routes
@app.route('/create_book', methods=['POST'])
@role_required('faculty', 'staff')
def create_book():
    data = request.json
    try:
        # Use keyword arguments for instantiation
        new_book = Book(title=data['title'], author=data['author'], isbn=data['isbn'])
        new_book.save()  # Save the new book document to MongoDB
        return jsonify({'message': 'Book created successfully'}), 201
    except KeyError as e:
        return jsonify({'error': f'Missing key in data: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 50


@app.route('/borrow_book', methods=['POST'])
def borrow_book():
    data = request.json
    user_name = data['user_name']
    book_title = data['book_title']

    user = users_collection.find_one({"name": user_name})
    book = books_collection.find_one({"title": book_title})

    if not user or not book or book.get('borrowed', False):
        return jsonify({'message': 'User, book not found, or book already borrowed'}), 404

    # Mark book as borrowed and set due date
    due_date = datetime.datetime.now() + datetime.timedelta(days=14)  # 2 weeks duration
    books_collection.update_one({'_id': book['_id']}, {'$set': {'borrowed': True, 'due_date': due_date}})

    # Add book to user's borrowed books
    users_collection.update_one({'_id': user['_id']}, {'$push': {'borrowed_books': book['_id']}})

    return jsonify({'message': 'Book borrowed successfully', 'due_date': due_date.strftime('%Y-%m-%d')}), 200


@app.route('/return_book', methods=['POST'])
def return_book():
    data = request.json
    user_name = data['user_name']
    book_title = data['book_title']

    user = users_collection.find_one({"name": user_name})
    book = books_collection.find_one({"title": book_title})

    if not user or not book or not book.get('borrowed', False):
        return jsonify({'message': 'User, book not found, or book not borrowed'}), 404

    # Mark book as not borrowed
    books_collection.update_one({'_id': book['_id']}, {'$set': {'borrowed': False, 'due_date': None}})

    # Remove book from user's borrowed books
    users_collection.update_one({'_id': user['_id']}, {'$pull': {'borrowed_books': book['_id']}})

    return jsonify({'message': 'Book returned successfully'}), 200


@app.route('/reserve_book', methods=['POST'])
def reserve_book():
    data = request.json
    user_name = data['user_name']
    book_title = data['book_title']

    user = users_collection.find_one({"name": user_name})
    book = books_collection.find_one({"title": book_title})

    if not user or not book or book.get('reserved', False):
        return jsonify({'message': 'User, book not found, or book already reserved'}), 404

    # Mark book as reserved
    reservation_date = datetime.datetime.now()
    books_collection.update_one({'_id': book['_id']},
                                {'$set': {'reserved': True, 'reservation_date': reservation_date}})

    # Add book to user's reserved books
    users_collection.update_one({'_id': user['_id']}, {'$push': {'reserved_books': book['_id']}})

    return jsonify({'message': 'Book reserved successfully'}), 200


@app.route('/calculate_fines', methods=['GET'])
def calculate_fines():
    data = request.json
    user_name = data['user_name']

    user = users_collection.find_one({"name": user_name})
    if not user:
        return jsonify({'message': 'User not found'}), 404

    fines = 0
    for book_id in user.get('borrowed_books', []):
        book = books_collection.find_one({'_id': book_id})
        if book and book.get('due_date') and book['due_date'] < datetime.datetime.now():
            overdue_days = (datetime.datetime.now() - book['due_date']).days
            fines += 1 * overdue_days  # Assuming fine is $1 per day

    return jsonify({'message': 'Fines calculated successfully', 'fines': fines}), 200


# Kafka Example Route
@app.route('/send_message', methods=['POST'])
def send_message():
    try:
        data = request.json
        message = data.get('message')
        producer.send('library_topic', message.encode('utf-8'))
        return jsonify({'message': 'Message sent to Kafka'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Testing mongoDB
@app.route('/test_mongodb', methods=['GET'])
def test_mongodb():
    try:
        # Assuming you have a collection named 'users'
        users_count = users_collection.count_documents({})
        return jsonify({'message': f'MongoDB connection successful. Users count: {users_count}'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# testing kafka
@app.route('/test_kafka', methods=['GET'])
def test_kafka():
    try:
        producer.send('test_topic', b'Test message')
        producer.flush()
        return jsonify({'message': 'Kafka message sent successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/test')
def test():
    return 'Test route is working', 200


if __name__ == '__main__':
    app.run(debug=True)
