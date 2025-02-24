from flask import Flask
from flask_restx import Api

from app.api.util.base_dto import BaseDto
from app.api.v1.controllers.user import ns as user_ns
from app.api.v1.controllers.role import ns as role_ns
from app.api.v1.controllers.file import ns as file_ns
from app.api.v1.controllers.auth import ns as auth_ns
from app.api.v1.controllers.tool import ns as tool_ns


api = Api(
    version="latest",
    title="🎉 接口汇总 🎉",
    description="🎉 接口汇总文档 🎉",
    authorizations={
            "Bearer Auth": {
                "type": "apiKey",
                "in": "header",
                "name": "Authorization",
                "description": "使用Swagger测试需要加前缀. Example: Bearer token",
            }
    },
    doc="/",
    security="Bearer Auth"
)


def init_restx(app: Flask) -> None:

    api.add_namespace(BaseDto.ns, path='/api/v1/base')
    api.add_namespace(user_ns, path='/api/v1/user')
    api.add_namespace(role_ns, path='/api/v1/role')
    api.add_namespace(file_ns, path='/api/v1/file')
    api.add_namespace(auth_ns, path='/api/v1/auth')
    api.add_namespace(tool_ns, path='/api/v1/tool')

    api.init_app(app)
