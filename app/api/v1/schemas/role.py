from ..models.role import RoleModel
from app.plugin.init_marshmallow import ma

class RoleSchema(ma.SQLAlchemyAutoSchema):
    """
    角色的序列化模型，用于将角色对象转换为JSON格式。
    """
    class Meta:
        model = RoleModel
        load_instance = True

