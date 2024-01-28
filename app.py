from flask import Flask
from mongoengine import connect
from flask_jwt_extended import JWTManager
from kafka import KafkaProducer
from pymongo import MongoClient

from config import DevelopmentConfig

# Initialize Flask app
app = Flask(__name__)

# Load configuration from DevelopmentConfig class
app.config.from_object(DevelopmentConfig)

# MongoDB and MongoEngine configuration
app.config["MONGODB_SETTINGS"] = {
    'db': 'librarydata',  # Name of the database
    'host': 'localhost',  # Host where MongoDB is running
    'port': 27017         # Port on which MongoDB is listening
}
connect(**app.config["MONGODB_SETTINGS"])  # Establish a connection to MongoDB

# Flask and JWT configuration
app.config['SECRET_KEY'] = 'Library'  # Replace with a strong secret key
app.config['JWT_SECRET_KEY'] = 'AIN3005'  # Replace with a strong JWT secret key
jwt = JWTManager(app)  # Initialize Flask JWT manager

# Kafka Producer setup
producer = KafkaProducer(bootstrap_servers=['localhost:9092'])

# Setup native MongoDB client
client = MongoClient('localhost', 27017)  # MongoClient for interacting with MongoDB
db = client.librarydata  # Reference to the 'librarydata' database
users_collection = db.users  # Reference to the 'users' collection
books_collection = db.books  # Reference to the 'books' collection

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)  # Start the Flask application
