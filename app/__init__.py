from flask import Flask
from .core.database import db, migrate
from .auth.routes import auth_bp
from .cadastros.routes import cadastros_bp

def create_app():
    app = Flask(__name__)
    
    app.config.from_object('app.core.config.Config')

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(auth_bp)
    app.register_blueprint(cadastros_bp)

    return app
