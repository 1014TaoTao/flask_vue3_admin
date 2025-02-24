import os

from flask import Blueprint, abort, request
from flask_jwt_extended import jwt_required
from flask_restx import Resource

from app.config.setting import Config
from app.api.common.response import exception_response, success_response
from app.api.util.base_dto import BaseDto
from ..dto.file import FileDto

ns = FileDto.ns
bp = Blueprint('file', __name__, url_prefix='/api/v1')

@ns.marshal_with(BaseDto.response_parser)
@ns.route('/upload')
class FileController(Resource):
    @jwt_required()
    @ns.doc(description='单文件上传接口')
    @ns.expect(FileDto.upload_parser, validate=True)
    def post(self):
        """单文件上传"""
        try:
            file = request.files.get('file')
            ns.logger.info("【单文件上传，文件名】：%s",file.filename)
            if not file:
                abort(400, '文件不存在')
            if file.filename.split('.')[-1].lower() not in Config.ALLOWED_EXTENSIONS:
                abort(400, '文件类型不支持')
            if file.content_length > Config.MAX_FILE_SIZE:
                abort(400, '文件大小超过限制')
            file_path = os.path.join(Config.UPLOAD_FILE_PATH, file.filename)
            file.save(file_path)  #指定保存路径
            return success_response(message="上传文件成功", data=file.filename)
        except Exception as e:
            return exception_response(message="服务器异常", data=str(e))

@ns.marshal_with(BaseDto.response_parser)
@ns.route('/uploads')
class FilesController(Resource):
    @jwt_required()
    @ns.doc(description='多文件上传接口')
    @ns.expect(FileDto.uploads_parser, validate=True)
    def post():
        """多文件上传"""
        try:
            files = request.files.getlist('files')
            ns.logger.info("【多文件上传，文件名】：%s",[file.filename for file in files])
            if not files:
                abort(400, '文件不存在')
            for file in files:
                if file and file.filename.split('.')[-1].lower() not in Config.ALLOWED_EXTENSIONS:
                    abort(400, '文件类型不支持')
                if file and file.content_length > Config.MAX_FILE_SIZE:
                    abort(400, '文件大小超过限制')
                file_path = os.path.join(Config.UPLOAD_FILE_PATH, file.filename)
                file.save(file_path) #指定保存路径
                # 读取文件内容
                # with open(file_path, 'rb') as f:
                #     file_content = f.read()
                #     print(file_content)
            return success_response(message="上传文件成功", data=aaa)
        except Exception as e:
            return exception_response(message="服务器异常", data=str(e))

