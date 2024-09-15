from flask import g
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


class ModelBase(db.Model):
    __abstract__ = True


def set_query(query):
    g.query = query


def get_query():
    return g.get("query", None)
