from app.api.util.base_model import BaseModel  # 导入基础模型类
from app.plugin.init_sqlalchemy import db  # 导入初始化sqlalchemy的模块


# 角色模型
class RoleModel(BaseModel, db.Model):
    __tablename__ = 'roles'  # 表名
    name = db.Column(db.String(32), unique=True, nullable=False, comment='名称')  # 角色名称
    permissions = db.Column(db.Integer)
    users = db.relationship('UserModel', backref='role', lazy='dynamic')
    
    def __repr__(self):
        return 'RoleModel:%s'%self.name