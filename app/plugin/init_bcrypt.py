from flask import Flask
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

def init_bcrypt(app: Flask) -> None:
    """Initialize Flask-Bcrypt extension."""
    bcrypt.init_app(app)