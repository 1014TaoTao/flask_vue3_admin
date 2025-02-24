from flask import Flask

from app.api.v1.controllers.user import bp as user_bp
from app.api.v1.controllers.role import bp as role_bp
from app.api.v1.controllers.file import bp as file_bp
from app.api.v1.controllers.auth import bp as auth_bp
from app.api.v1.controllers.tool import bp as tool_bp


def init_blueprints(app: Flask) -> None:
    """注册蓝图"""    
    app.register_blueprint(user_bp)
    app.register_blueprint(role_bp)
    app.register_blueprint(file_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(tool_bp)

