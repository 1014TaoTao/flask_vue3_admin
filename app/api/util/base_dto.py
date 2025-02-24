from flask_restx import Namespace, fields, reqparse

class BaseDto:
    ns = Namespace(name="公共部分dto")
    
    page_parser = ns.parser()
    page_parser.add_argument('page_no', location='args', type=int, required=True, help='页码', default=1)
    page_parser.add_argument('page_size', location='args', type=int, required=True, help='每页条数', default=10)
    page_parser.add_argument('filters', location='args', type=str, required=False, help='筛选条件', default='{"name":"demo","description":"备注"}')
    page_parser.add_argument('order_by', location='args', type=str, required=False, help='筛选条件', default='["create_at","asc"]')

    delete_detail_parser = reqparse.RequestParser()
    delete_detail_parser.add_argument('id', location='path',type=int, required=True, help='对象ID', default=1)

    response_parser = ns.model('ResponseSchema', {
        'code': fields.Integer(description='响应状态码'),
        'msg': fields.String(description='响应消息'),
        'data': fields.Raw(description='响应数据'),
    })