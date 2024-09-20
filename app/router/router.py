from flask import Flask
from app.modules.auth.routes import auth_bp
from app.modules.cadastros.routes import cadastros_bp
from app.modules.integracoes.routes import integracoes_bp


def register_routes(app: Flask):
    app.register_blueprint(auth_bp)
    app.register_blueprint(cadastros_bp)
    app.register_blueprint(integracoes_bp)
