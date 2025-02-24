from flask import Flask
from flask_cors import CORS

cors = CORS(resources=r'/*')


def init_cors(app: Flask) -> None:
    """跨域中间件"""
    cors.init_app(app=app)
