import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_CONNECT')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_TOKEN_LOCATION = ["cookies"]
