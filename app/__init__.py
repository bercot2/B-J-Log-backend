from flask import Flask
from flask_cors import CORS

from .exceptions.config_exceptions import init_error_handlers
from .router.router import register_routes
from .core.database import db, migrate
from .modules.auth import jwt, register_authentication_hooks


def create_app():
    app = Flask(__name__)
    CORS(
        app,
        supports_credentials=True,
        resources={
            r"/*": {"origins": ["http://localhost:8081", "http://BJLogfrontend:3000"]}
        },
    )

    app.config.from_object('app.core.config.Config')

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    register_routes(app)

    register_authentication_hooks(app)
    init_error_handlers(app)

    return app
