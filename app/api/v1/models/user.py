from app.api.util.base_model import BaseModel  # 导入基础模型类
from app.plugin.init_sqlalchemy import db  # 导入初始化sqlalchemy的模块
from app.plugin.init_bcrypt import bcrypt  # 导入bcrypt用于密码哈希


# 用户模型
class UserModel(BaseModel, db.Model):
    """
    用户模型，用于表示系统中的用户。
    """
    __tablename__ = 'users'  # 表名
    name = db.Column(db.String(15), unique=True, index=True, nullable=False, comment='用户名')  # 用户名
    password_hash = db.Column(db.String(128), unique=True, nullable=False, comment='密码')  # 密码哈希值
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)

    def __repr__(self):
        return 'UserModel:%s'%self.name
    
    def set_password(self, password):
        # 设置新密码
        self.password_hash = bcrypt.generate_password_hash(password, rounds=12).decode("utf-8") if password else None

    @staticmethod
    def validate_username(username):
        # 验证用户名是否符合要求
        if len(username) > 15:
            raise ValueError("用户名长度超过限制")
        return username

    def check_password(self, password):
        # 验证密码是否正确
        return bcrypt.check_password_hash(self.password_hash, password)
    