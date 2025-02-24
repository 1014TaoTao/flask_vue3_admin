import datetime
from flask import Blueprint, json, request
from flask_restx import Resource
from flask_jwt_extended import jwt_required

from app.plugin.init_cache import cache
from app.plugin.init_sqlalchemy import db
from app.api.common.response import exception_response, success_response, error_response
from app.api.util.base_serialize import model_to_dict, dict_to_model
from app.api.util.base_dto import BaseDto
from ..dto.user import UserDto
from ..models.user import UserModel
from ..schemas.user import UserSchema

ns = UserDto.ns
bp = Blueprint("user", __name__, url_prefix="/api/v1")

@ns.marshal_with(BaseDto.response_parser)
@ns.route('')
class UserListResource(Resource):
    """用户
    分页查询、创建、更新
    """
    @jwt_required()
    @ns.doc(description='分页查询接口')
    @ns.expect(BaseDto.page_parser, validate=True)
    def get(self):
        """
        获取用户列表
        """
        args = request.args.to_dict()
        ns.logger.info('查询用户【请求参数】: %s', args)
        try:
            page_no = int(args.get('page_no', 1))
            page_size = int(args.get('page_size', 10))
            filters = json.loads(args.get('filters', "{}"))
            order_by = json.loads(args.get('order_by', "[]"))
            
            results= UserModel.paginate(page_no, page_size, filters, order_by)
            
            items = [model_to_dict(s=UserSchema,m=item) for item in results['items']]
        
            results['items'] = items
            return success_response(message='查询成功', data=results)
        except Exception as e:
            return exception_response(message='查询异常', data=str(e))
    
    @jwt_required()
    @ns.doc(description='新增接口')
    @ns.expect(UserDto.user_parser, validate=True)
    def post(self):
        """
        创建用户
        """
        ns.logger.info('创建用户【请求参数】:%s - %s', type(request.get_json()),request.get_json())
        args = request.get_json()
        try:
            name = args.get('name')
            existing_user = UserModel.query.filter(UserModel.name == name).first()
            if existing_user:
                ns.logger.info('【判断用户是否存在】: %s', existing_user)
                return error_response(message='名称已存在')

            int(args['role_id'])
            
            user_model = dict_to_model(s=UserSchema,d=args)
            user_model.set_password(args.get('password_hash'))
            
            db.session.add(user_model)
            db.session.commit()
            return success_response(message='新增成功', data=args)
        except Exception as e:
            db.session.rollback()
            return exception_response(message='新增异常', data=str(e))
    

@ns.marshal_with(BaseDto.response_parser)
@ns.route('/<int:id>')
class UserResource(Resource):
    @jwt_required()
    @ns.doc(description='详情接口')
    def get(self,id):
        """
        获取用户详情
        """
        ns.logger.info('用户详情【请求参数】: %s', id)
        try:
            user_mdoel = UserModel.query.get(int(id))
            if not user_mdoel:
                return error_response(message='用户不存在')
            user_dict = model_to_dict(s=UserSchema,m=user_mdoel)
            return success_response(message='查看详情成功', data=user_dict)
        except Exception as e:
            return exception_response(message='查看详情异常', data=str(e))
    
    @jwt_required()
    @ns.doc(description='更新接口')
    @ns.expect(UserDto.user_parser, validate=True)
    def put(self,id):
        """
        更新用户
        """
        ns.logger.info('request.get_json()更新用户【请求参数】: %s', request.get_json())
        args = request.get_json()
        name = args.get('name')
        try:
            user = UserModel.query.get(int(id))
            if not user:
                return error_response(message='用户不存在')
            existing_user = UserModel.query.filter(((UserModel.id != id) & (UserModel.name == name))).first()
            if existing_user:
                return error_response(message='用户名称已存在')
            # 反序列化校验字段
            user.name = args.get('name')
            user.set_password(args.get('password_hash'))
            user.role_id = args.get('role_id')
            user.description = args.get('description')
            user.update_at = datetime.datetime.now()
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
        删除用户
        """
        ns.logger.info('删除用户【请求参数】: %s', id)
        try:
            user = UserModel.query.get(int(id))
            if not user:
                return error_response(message='用户不存在')
            db.session.delete(user)
            db.session.commit()
            return success_response(message='删除成功', data=model_to_dict(s=UserSchema,m=user))
        except Exception as e:
            db.session.rollback()
            return exception_response(message='删除异常', data=str(e))