from ..api.v1.models.role import RoleModel
from ..api.v1.models.user import UserModel
from ..api.v1.models.tool import ToolModel
from ..api.common.const import ROLE_USER_PERMISSIONS,ROLE_ADMIN_PERMISSIONS
from .init_sqlalchemy import db
from .init_bcrypt import bcrypt

code = """
import sqlite3
import json

db_path = '/Users/tao/workspace/mycode/my_demo_project/flaskproject/backend/dev_sql.db'

def query_to_json(params):
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(params)
            results = cursor.fetchall()
            column_names = [description[0] for description in cursor.description]
            json_results = [dict(zip(column_names, row)) for row in results]
            return json.dumps(json_results, ensure_ascii=False)
    except Exception as e:
        return f'Error connect db: {e}'
"""


user_passwords = ['admin123456', 'demo123456', 'test123456']
hashed_passwords = [bcrypt.generate_password_hash(password).decode('utf-8') for password in user_passwords]

admin_role = RoleModel(name='admin', permissions=ROLE_ADMIN_PERMISSIONS, description='全功能访问，包括创建、读取、更新和删除')
user_role = RoleModel(name='user', permissions=ROLE_USER_PERMISSIONS, description='只读权限，只能浏览')

amdin_user = UserModel(name='admin', password_hash=hashed_passwords[0], role=admin_role, description='系统管理员')
demo_user = UserModel(name='demo', password_hash=hashed_passwords[1], role=user_role, description='演示用户')
test_user = UserModel(name='test', password_hash=hashed_passwords[2], role=user_role, description='测试用户')

test_tool = ToolModel(name='query_to_json', function_name='query_to_json', description='输入sql语句，查询数据', params='sql_query',code=code)

init_all_data =[
    admin_role,
    user_role,
    amdin_user,
    demo_user,
    test_user,
    test_tool
]
def init_databases(app):
    try:
        db.session.add_all(init_all_data)
        db.session.commit()
        app.logger.info(f'System initialization data configured: {init_all_data}')
        db.session.close()
    except Exception as e:
        # 插入失败自动回滚
        db.session.rollback()
        raise e
    