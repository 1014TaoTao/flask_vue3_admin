from flask import Flask
from flask_jwt_extended import JWTManager

jwt = JWTManager()


def init_jwt(app: Flask) -> None:
    """
    Initialize JWT extension.
    """
    jwt.init_app(app)
