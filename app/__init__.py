from flask import Flask

from app.exceptions.config_exceptions import init_error_handlers
from router.router import register_routes
from .core.database import db, migrate
from .auth import jwt, register_authentication_hooks


def create_app():
    app = Flask(__name__)

    app.config.from_object('app.core.config.Config')

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    register_routes(app)

    register_authentication_hooks(app)
    init_error_handlers(app)

    return app
