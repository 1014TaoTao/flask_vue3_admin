from typing import List
from flask_restx import Namespace
from werkzeug.datastructures import FileStorage


class FileDto:
    ns = Namespace(name="文件管理")

    # 单文件上传的请求解析器
    upload_parser = ns.parser()
    upload_parser.add_argument(name='file',type=FileStorage,location='files',required=True,help='缺少文件')

    # 多文件上传的请求解析器
    uploads_parser = ns.parser()
    uploads_parser.add_argument(name='files',type=FileStorage,action='append',location='files',required=True,help='缺少文件')
