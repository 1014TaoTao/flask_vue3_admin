from flask import Flask

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_sqlalchemy(app: Flask):
    """数据库中间件"""
    try:
        db.init_app(app=app)
        with app.app_context():
            try:
                db.engine.connect()
                # 数据库初始化
                db.drop_all()
                db.create_all()
            except Exception as e:
                exit(f"数据库连接失败: {e}")
    except Exception as e:
        raise RuntimeError(f"数据库连接异常: {e}")
    
