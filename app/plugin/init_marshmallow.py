from flask import Flask
from flask_marshmallow import Marshmallow

ma = Marshmallow()

def init_marshmallow(app: Flask) -> None:
    ma.init_app(app)