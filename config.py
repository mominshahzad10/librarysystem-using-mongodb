import os


class Config:
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a_very_secret_key_change_it'

    # MongoDB settings
    MONGO_URI = os.environ.get('MONGO_URI') or 'mongodb://localhost:27017/librarydata'

    # Kafka settings
    KAFKA_BROKER = os.environ.get('KAFKA_BROKER') or 'localhost:9092'
    KAFKA_TOPIC = os.environ.get('KAFKA_TOPIC') or 'library_topic'

    # JWT settings
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'another_very_secret_key_change_it'
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # Token expiration in seconds


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


class TestingConfig(Config):
    TESTING = True
    MONGO_URI = 'mongodb://localhost:27017/librarydata'
