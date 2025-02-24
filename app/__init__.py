from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix

from .plugin.init_cache import init_cache
from .plugin.init_cors import init_cors
from .plugin.init_jwt import init_jwt
from .plugin.init_marshmallow import init_marshmallow
from .plugin.init_restx import init_restx
from .plugin.init_migrate import init_migrate
from .plugin.init_sqlalchemy import init_sqlalchemy
from .plugin.init_blueprints import init_blueprints
from .plugin.init_bcrypt import init_bcrypt
from .plugin.init_databases import init_databases

from .config.setting import config_by_name


def create_app(env_name):
    """工程模式"""
    app = Flask(__name__)
    app.wsgi_app = ProxyFix(app.wsgi_app)

    # 引入配置
    app.config.from_object(config_by_name[env_name])

    with app.app_context():
        # ===========注册flask插件===========
        init_sqlalchemy(app)  # orm注册
        init_migrate(app)  # 数据迁移
        init_restx(app)  # 注册restx
        init_marshmallow(app)  # 注册marshmallow
        init_cors(app)  # 开启跨域
        init_cache(app)  # 注册缓存
        init_bcrypt(app)    # 注册bcrypt
        init_jwt(app)    # 注册jwt
        # ===========注册蓝图===========
        init_blueprints(app)
        # ===========初始化脚本===========
        init_databases(app)

    return app
