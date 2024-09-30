import os

from datetime import timedelta
from dotenv import load_dotenv

env = os.getenv("FLASK_ENV")
dotenv_path = f".env.{env}"

load_dotenv(dotenv_path, override=True)

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_CONNECT')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_TOKEN_LOCATION = ["cookies"]
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=2)
    JWT_COOKIE_CSRF_PROTECT = True
    JWT_ACCESS_CSRF_HEADER_NAME = "X-CSRF-TOKEN"
    PERMANENT_SESSION_LIFETIME = timedelta(hours=2)
    SESSION_PERMANENT = False
    SESSION_COOKIE_SECURE = os.getenv("SESSION_COOKIE_SECURE", "False").lower() in [
        "true"
    ]
    SESSION_COOKIE_HTTPONLY = True
