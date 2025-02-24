from app.plugin.init_marshmallow import ma

from ..models.user import UserModel


class UserSchema(ma.SQLAlchemyAutoSchema):
    """
    用户的序列化模型，用于将用户对象转换为JSON格式。
    """
    class Meta:
        model = UserModel
        load_instance = True  # 允许反序列化为模型实例
        include_fk = True  # 包含外键


