import datetime
from flask import Blueprint, jsonify, request
from flask_restx import Resource
from flask_jwt_extended import create_access_token,create_refresh_token, get_jwt, jwt_required, get_jwt_identity

from app.api.common.response import error_response, exception_response, success_response
from app.api.util.base_serialize import model_to_dict, dict_to_model
from app.api.util.base_dto import BaseDto
from ..models.user import UserModel
from ..dto.auth import AuthDto
from ..models.user import UserModel
from ..schemas.user import UserSchema
from app.plugin.init_sqlalchemy import db
from app.plugin.init_jwt import jwt

ns = AuthDto.ns
bp = Blueprint("auth", __name__, url_prefix="/api/v1")

# 过期令牌
@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        'message': 'token已失效',
        'error': 'token_expired'
    }), 401

# 无效令牌
@jwt.invalid_token_loader
def invalid_token_callback():
    return jsonify({
        'message': 'token无效.',
        'error': 'invalid_token'
    }), 401


@ns.marshal_with(BaseDto.response_parser)
@ns.route("/login")
class AuthLoginController(Resource):

    @ns.doc(description='登陆接口')
    @ns.expect(AuthDto.login_parser, validate=True)
    def post(self):
        """ 登陆 """
        try:
            login_data = request.form
            ns.logger.info('用户登陆【请求参数】: %s', login_data)
            username = login_data.get('username')
            password = login_data.get('password')
            
            #找到用户资料
            user = UserModel.query.filter_by(name=username).first()
            if not user :
                return error_response(message='登陆失败，用户不存在', data=login_data)
            if user.check_password(password):
                #生成token，认证令牌和刷新令牌
                access_token = create_access_token(identity=user.id,fresh=True)
                refresh_token = create_refresh_token(user.id)
                data = {
                        'access_token': f'Bearer {access_token}',
                        'refresh_token': f'Bearer {refresh_token}',
                        'user': model_to_dict(s=UserSchema, m=user)
                    }
                return success_response(message='登陆成功', data=data)
            else:
                return error_response(message='登陆失败，密码错误', data=login_data)
        except Exception as e:
            return exception_response(message='登陆异常', data=str(e))


@ns.marshal_with(BaseDto.response_parser)
@ns.route("/register")
class AuthRegisterController(Resource):

    @ns.doc(description='注册接口')
    @ns.expect(AuthDto.auth_register, validate=True)
    def post(self):
        """ 注册 """
        try:
            register_data = request.get_json()
            ns.logger.info('用户注册【请求参数】: %s', register_data)
            if not register_data:
                return error_response(message='请求数据为空', data=register_data)
            existing_user = UserModel.query.filter_by(name=register_data.get('name')).first()
            if existing_user:
                return error_response(message='名称已存在')
            #找到用户资料
            register_data['role_id'] = 2
            user_model = dict_to_model(s=UserSchema,d=register_data)
            user_model.set_password(register_data.get('password_hash'))
            db.session.add(user_model)
            db.session.commit()
            return success_response(message='注册成功', data=register_data)
        except Exception as e:
            return exception_response(message='注册异常', data=str(e))

@ns.marshal_with(BaseDto.response_parser)
@ns.route('/protected')
class AuthProtectedController(Resource):
    
    @ns.doc(description='获取当前登陆信息')
    @jwt_required(refresh=True)
    def get(self):
        """获取当前登陆用户信息"""
        try:
            current_user = get_jwt_identity()
            ns.logger.info('获取当前登陆用户信息【请求参数】: %s', current_user)
            return success_response(message='获取成功', data=current_user)
        except Exception as e:
            return exception_response(message='获取异常', data=str(e))

@ns.marshal_with(BaseDto.response_parser)
@ns.route('/refresh')
class AuthRefreshController(Resource):

    @ns.doc(description='刷新token')
    @jwt_required(refresh=True)
    def post(self):
        """刷新token"""
        # 使用刷新JWT来获取普通JWT  前提是已经调用了 /login 接口 携带 refresh_token请求该接口
        try:
            identity = get_jwt_identity()
            access_token = create_access_token(identity=identity)
            data = {'access_token': f"Bearer {access_token}"}
            ns.logger.info('刷新token【请求参数】: %s', data)
            return success_response(message='刷新成功', data=data)
        except Exception as e:
            return exception_response(message='刷新异常', data=str(e))
