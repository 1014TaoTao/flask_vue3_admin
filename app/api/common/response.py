from http import HTTPStatus
from typing import Any

from flask import current_app, jsonify, abort, g
from flask_restx import Namespace, fields, reqparse


ns = Namespace(name="代码响应")

response_parser = ns.model('ResponseSchema', {
    'code': fields.Integer(description='响应状态码'),
    'msg': fields.String(description='响应消息'),
    'data': fields.Raw(description='响应数据'),
})


def success_response(
    data=None,
    status_code=HTTPStatus.OK.value,
    message=HTTPStatus.OK.description
):
    if isinstance(data, bytes):
        data = data.decode("utf-8")  # 假设数据是UTF-8编码
    response: dict = {
        "code": status_code,
        "msg": message,
        "data": data
    }
    current_app.logger.info('Success: %s', response)
    return response


def error_response(
    data=None,
    status_code=HTTPStatus.BAD_REQUEST.value,
    message=HTTPStatus.BAD_REQUEST.description
):
    if isinstance(data, bytes):
        data = data.decode("utf-8")  # 假设数据是UTF-8编码
    response: dict = {
        "code": status_code,
        "msg": message,
        "data": data
    }
    current_app.logger.error('Fail: %s', response)
    return response


def exception_response(
    data=None,
    status_code=HTTPStatus.INTERNAL_SERVER_ERROR.value,
    message=HTTPStatus.INTERNAL_SERVER_ERROR.description
):
    if isinstance(data, bytes):
        data = data.decode("utf-8")  # 假设数据是UTF-8编码
    response: dict = {
        "code": status_code,
        "msg": message,
        "data": data
    }
    current_app.logger.exception('Error: %s', response)
    return response
