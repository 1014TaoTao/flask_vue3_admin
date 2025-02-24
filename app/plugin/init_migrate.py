from flask import Flask
from flask_migrate import Migrate

from .init_sqlalchemy import db

migrate = Migrate(db=db)


def init_migrate(app: Flask) -> None:
    """数据迁移中间件"""
    migrate.init_app(app=app)
