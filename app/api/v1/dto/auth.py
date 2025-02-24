from flask_restx import Namespace, fields


class AuthDto:
    ns = Namespace(name="权限模块")


    auth_register = ns.model(
        "Registration data",
        {
            'name': fields.String(required=True, description="用户名称"),
            'password_hash': fields.String(required=True, description="用户密码"),
            'description': fields.String(description="备注信息"),
        },
    )

    auth_success = ns.model(
        "Auth success response",
        {
            "status": fields.Boolean,
            "message": fields.String,
            "access_token": fields.String,
            "user": fields.Nested(auth_register),
        },
    )
    
    login_parser = ns.parser()
    login_parser.add_argument('username', type=str, location='form', required=True, help='输入合法的用户名',default ='admin')
    login_parser.add_argument('password', type=str, location='form', required=True, help='输入安全的密码',default = 'admin123456')
