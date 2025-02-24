from flask_restx import Namespace, fields

class UserDto:
    ns = Namespace(name="用户管理")

    
    user_parser = ns.model('CreateUserSchema', {
        'name': fields.String(required=True, description="用户名称"),
        'password_hash': fields.String(required=True, description="用户密码"),
        'role_id': fields.Integer(required=True, description="绑定角色"),
        'description': fields.String(description="备注信息"),
    })
