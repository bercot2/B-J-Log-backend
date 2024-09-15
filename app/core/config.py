import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_CONNECT')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SECRET_KEY = os.getenv('SECRET_KEY', 'sua_chave_super_secreta')
    # JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt_secreta')
