import os
from datetime import date, timedelta
# 导入基础的配置类和必要的环境变量

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# 获取应用的基础目录路径


class Config(object):
    """
    应用的基础配置类，包含权限配置、异常处理、日志配置等。

    属性:
    - SECRET_KEY: 应用的密钥，用于加密。
    - JWT_SECRET_KEY: JWT认证的密钥。
    - JWT_EXPIRATION_DELTA: JWT令牌的过期时间。
    - JWT_ACCESS_TOKEN_EXPIRES: 访问令牌的过期时间。
    - JWT_REFRESH_TOKEN_EXPIRES: 刷新令牌的过期时间。
    - PROPAGATE_EXCEPTIONS: 是否允许异常传播。
    - LOGS_DIR: 日志文件存储目录。
    - LOG_DATEFMT: 日志文件的时间格式。
    - LOG_FORMAT: 日志的格式化字符串。
    - LOG_FILENAME: 日志文件的名称。
    - LOG_FILEPATH: 日志文件的完整路径。
    """
    # 权限配置
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", os.urandom(24))
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access']
    JWT_EXPIRATION_DELTA = timedelta(hours=1)
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30) # 设置普通JWT过期时间
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(minutes=30) # 设置刷新JWT过期时间
    # JWT_HEADER_TYPE = 'JWT'  # 可以修改 请求头中 ，token字符串的 前缀
    # 默认   Authorization: Bearer <token>
    # 异常处理
    PROPAGATE_EXCEPTIONS = True
    # 日志配置
    LOGS_DIR = os.path.join(BASE_DIR, '../..', 'logs')
    if not os.path.exists(LOGS_DIR):
        os.makedirs(LOGS_DIR)
    LOG_DATEFMT = '%Y-%m-%d %H:%M:%S %a'
    LOG_FORMAT = '[%(asctime)s] - [%(levelname)s] - [%(name)s:%(filename)s:%(funcName)s:%(lineno)d]: %(message)s'
    LOG_FILENAME = date.today().strftime(r'%Y-%m-%d.log')
    LOG_FILEPATH = os.path.join(LOGS_DIR, LOG_FILENAME)
    import logging
    logging.basicConfig(
        level=logging.INFO,
        format=LOG_FORMAT,
        datefmt=LOG_DATEFMT,
        handlers=[
            logging.FileHandler(filename=LOG_FILEPATH),
            logging.StreamHandler()
        ]
    )
    # 上传文件
    UPLOAD_FILE_PATH = os.path.join(BASE_DIR, '../..', 'data')
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB


class DevelopmentConfig(Config):
    """
    开发环境的配置类。

    属性:
    - DEBUG: 是否开启调试模式。
    - SQLALCHEMY_DATABASE_URI: 数据库的URI。
    - SQLALCHEMY_TRACK_MODIFICATIONS: 是否跟踪模型修改。
    - SQLALCHEMY_ECHO: 是否显示SQL语句。
    - SQLALCHEMY_COMMIT_ON_TEARDOWN: 请求结束是否提交数据库改动。
    """
    # 打开调试模式
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, '../..', 'dev_sql.db')}"
    # 禁用SQLAlchemy对追踪对象的修改并且发送信号
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 操作数据库时显示原始SQL语句
    SQLALCHEMY_ECHO = False
    # 每次请求结束后自动提交数据库中的改动
    SQLALCHEMY_COMMIT_ON_TEARDOWN = False
    # 开启SQLAlchemy的查询记录功能
    SQLALCHEMY_RECORD_QUERIES= False  
    
    """ 
    # 配置数据库连接池
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 10,
        'pool_recycle': 3600,
    }
    # 配置多个数据库连接
    SQLALCHEMY_BINDS = {
        'database1': 'postgresql://user:pass@host1/dbname1',
        'database2': 'mysql://user:pass@host2/dbname2',
    } """


class TestingConfig(Config):
    """
    测试环境的配置类。

    属性:
    - DEBUG: 是否开启调试模式。
    - TESTING: 是否为测试模式。
    - SQLALCHEMY_DATABASE_URI: 数据库的URI。
    - SQLALCHEMY_TRACK_MODIFICATIONS: 是否跟踪模型修改。
    - SQLALCHEMY_ECHO: 是否显示SQL语句。
    - SQLALCHEMY_COMMIT_ON_TEARDOWN: 请求结束是否提交数据库改动。
    """
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, '../..', 'test_sql.db')}"
    # 禁用SQLAlchemy对追踪对象的修改并且发送信号
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 操作数据库时显示原始SQL语句
    SQLALCHEMY_ECHO = False
    # 每次请求结束后自动提交数据库中的改动
    SQLALCHEMY_COMMIT_ON_TEARDOWN = False


class ProductionConfig(Config):
    """
    生产环境的配置类。

    属性:
    - DEBUG: 是否开启调试模式。
    - SQLALCHEMY_DATABASE_URI: 数据库的URI。
    - SQLALCHEMY_TRACK_MODIFICATIONS: 是否跟踪模型修改。
    - SQLALCHEMY_ECHO: 是否显示SQL语句。
    - SQLALCHEMY_COMMIT_ON_TEARDOWN: 请求结束是否提交数据库改动。
    - PRESERVE_CONTEXT_ON_EXCEPTION: 异常发生时是否保留上下文。
    """
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, '../..', 'prod_sql.db')}"
    # 禁用SQLAlchemy对追踪对象的修改并且发送信号
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 操作数据库时显示原始SQL语句
    SQLALCHEMY_ECHO = False
    # 每次请求结束后自动提交数据库中的改动
    SQLALCHEMY_COMMIT_ON_TEARDOWN = False
    PRESERVE_CONTEXT_ON_EXCEPTION = False


config_by_name = dict(
    development=DevelopmentConfig,
    testing=TestingConfig,
    production=ProductionConfig,
    default=DevelopmentConfig,
)
# 配置名字对应的配置类字典，用于根据环境选择配置。