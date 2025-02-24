import os
import sys

from app import create_app
from dotenv import load_dotenv


def main(argv=None):
    """
    应用程序的主入口函数。
    
    参数:
    - argv: 传入的命令行参数列表，默认为None，表示使用sys.argv。
    
    返回值:
    - 无返回值，直接启动Flask应用。
    """
    # 加载环境变量
    dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)
        falask_config = os.getenv("FLASK_CONFIG") or "default"
    else:
        raise RuntimeError("No .env file found, please create one.")
    
    # 处理命令行参数
    if argv is None:
        # 默认使用sys.argv作为命令行参数
        argv = sys.argv 
        # 创建Flask应用实例并运行
        app = create_app(falask_config)
        app.run(host='0.0.0.0', port='5001')

    # 默认开发环境配置及运行
    elif len(argv) < 2:
        app = create_app('development')
        app.run(host='0.0.0.0', port='5001')

    # 根据命令行参数选择环境并运行
    elif len(argv) == 2:
        app = create_app(argv[1])
        app.run(host='0.0.0.0', port='5001')
    else:
        raise RuntimeError("Unknown arguments in calling main.py!!!")

    
    
if __name__ == '__main__':
    # 当脚本直接运行时，调用主函数
    sys.exit(main())
    