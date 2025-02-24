import datetime
from flask import Blueprint, json, request
from flask_restx import Resource
from flask_jwt_extended import jwt_required

from app.plugin.init_cache import cache
from app.plugin.init_sqlalchemy import db
from app.api.common.response import exception_response, success_response, error_response
from app.api.util.base_serialize import model_to_dict, dict_to_model
from app.api.util.base_dto import BaseDto
from ..dto.role import RoleDto
from ..models.role import RoleModel
from ..schemas.role import RoleSchema

ns = RoleDto.ns
bp = Blueprint("role", __name__, url_prefix="/api/v1")

@ns.marshal_with(BaseDto.response_parser)
@ns.route('')
class RoleListResource(Resource):
    """角色
    分页查询、创建、更新
    """
    @jwt_required()
    @ns.doc(description='分页查询接口')
    @ns.expect(BaseDto.page_parser, validate=True)
    def get(self):
        """
        获取角色列表
        """
        args = request.args.to_dict()
        ns.logger.info('查询角色【请求参数】: %s', args)
        try:
            page = int(args.get('page', 1))
            per_page = int(args.get('per_page', 10))
            filters = json.loads(args.get('filters', "{}"))
            order_by = json.loads(args.get('order_by', "[]"))
            
            results= RoleModel.paginate(page, per_page, filters, order_by)
            
            items = [model_to_dict(s=RoleSchema,m=item) for item in results['items']]
        
            results['items'] = items
            
            return success_response(message='查询成功', data=results)
        except Exception as e:
            return exception_response(message='查询异常', data=str(e))
    
    @jwt_required()
    @ns.doc(description='新增接口')
    @ns.expect(RoleDto.role_parser, validate=True)
    def post(self):
        """
        创建角色
        """
        ns.logger.info('创建角色【请求参数】:%s - %s', type(request.get_json()),request.get_json())
        args = request.get_json()
        try:
            name = args.get('name')
            existing_role = RoleModel.query.filter(RoleModel.name == name).first()
            if existing_role:
                ns.logger.info('【判断角色是否存在】: %s', existing_role)
                return error_response(message='名称已存在')
            role_model = dict_to_model(s=RoleSchema,d=args)
            db.session.add(role_model)
            db.session.commit()
            return success_response(message='新增成功', data=args)
        except Exception as e:
            db.session.rollback()
            return exception_response(message='新增异常', data=str(e))


@ns.marshal_with(BaseDto.response_parser)
@ns.route('/<int:id>')
class RoleResource(Resource):
    @jwt_required()
    @ns.doc(description='详情接口')
    def get(self,id):
        """
        获取角色详情
        """
        ns.logger.info('角色详情【请求参数】: %s', id)
        try:
            role_mdoel = RoleModel.query.get(int(id))
            if not role_mdoel:
                return error_response(message='角色不存在')
            role_dict = model_to_dict(s=RoleSchema,m=role_mdoel)
            return success_response(message='查看详情成功', data=role_dict)
        except Exception as e:
            return exception_response(message='查看详情异常', data=str(e))
    
    @jwt_required()
    @ns.doc(description='更新接口')
    @ns.expect(RoleDto.role_parser, validate=True)
    def put(self,id):
        """
        更新角色
        """
        ns.logger.info('request.get_json()更新角色【请求参数】: %s', request.get_json())
        args = request.get_json()
        name = args.get('name')
        try:
            role = RoleModel.query.get(int(id))
            if not role:
                return error_response(message='角色不存在')
            # 反序列化校验字段
            role.name = args.get('name')
            role.permissions = args.get('permissions')
            role.description = args.get('description')
            role.update_at = datetime.datetime.now()
            db.session.merge
            db.session.commit()
            return success_response(message='更新成功', data=args)
        except Exception as e:
            db.session.rollback()
            return exception_response(message='更新异常', data=str(e))
    
    @jwt_required()
    @ns.doc(description='删除接口')
    def delete(self,id):
        """
        删除角色
        """
        ns.logger.info('删除角色【请求参数】: %s', id)
        try:
            role = RoleModel.query.get(int(id))
            if not role:
                return error_response(message='角色不存在')
            db.session.delete(role)
            db.session.commit()
            return success_response(message='删除成功', data=model_to_dict(s=RoleSchema,m=role))
        except Exception as e:
            db.session.rollback()
            return exception_response(message='删除异常', data=str(e))