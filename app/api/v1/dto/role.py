from flask_restx import Namespace, fields


class RoleDto:
    ns = Namespace(name="角色管理")

    role_parser = ns.model('CreateRoleSchema', {
        'name': fields.String(required=True, description="角色名称"),
        'permissions': fields.Integer(required=True, description="绑定权限"),
        'description': fields.String(description="备注信息"),
    })

