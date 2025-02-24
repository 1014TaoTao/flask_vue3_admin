#### 1、介绍
> my_demo_project：python的flask项目整合，打造团队工程项目规范

#### 2、软件架构
> 用到了flask、flask-restx、flask-migrate、flask-sqlalchemy、蓝图等技术


#### 3、安装教程

1.  启动项目直接运行：
flask db init
flask db migrate
flask db upgrade
2.  实现了User的增删改查，图片上传，附件上传等

#### 4、生成所有依赖

> pip freeze > requirements.txt 生成requirements.txt（虚拟环境所有依赖）
> pip install pipreqs
> pipreqs . --encoding=utf8  --force  生成requirements.txt（使用 pipreqs 扫描项目代码生成虚拟环境所有依赖）
> pip install portry
> poetry init
> poetry env list
> poetry env remove --all
> poetry env remove /full/path/to/python
>
> # 同时删除多个环境
> poetry env remove python3.6 python3.7 python3.8
> # 一次性删除全部环境 
> poetry env remove --all
> poetry shell 
> 	# 添加依赖
> poetry add <lib>
> # 添加dev依赖
> poetry add <lib> --dev  # poetry add package-name -D
> # 删除依赖
> poetry remove <lib>
> # 更新依赖
> poetry update
> # 锁定依赖版本
> poetry lock
> # 列出全部依赖项
> poetry show
> # 列出陈旧的依赖项
> poetry show --outdated
> # 搜索指定的包
> poetry search <name>
> poetry uninstall flask-restx
> 生成requirements.txt：poetry export -f requirements.txt -o requirements.txt --without-hashes --dev

构建打包
> pipenv install pyinstaller
> 将依赖包都安装完成后直接：pyinstaller -Fw -i xx.ico ./xxx.py
#### 5、技术细节

**基础装饰器说明**

```markdown
@api.route() 定义接口路由
@api.response() 定义各响应状态吗对应的类型
@api.model() 定义json类模型
@api.doc：定义接口文档
@api.expect：定义输入参数
@api.marshal_with：定义输出类型
```

**请求参数获取**

parser.add_argument() 类型

```python
'args': 从 URL 查询参数中获取参数值。
例如: ?name=John&age=30
'headers': 从 HTTP 请求头中获取参数值。
例如: X-API-Key: abc123
'json': 从 JSON 请求体中获取参数值。
例如: {"name": "John", "age": 30}
'form': 从表单数据中获取参数值。
例如: name=John&age=30
'files': 从文件上传中获取参数值。
例如: file=example.jpg
'path': 从 URL 路径中获取参数值。
例如: /users/123
'cookie': 从 HTTP Cookie 中获取参数值。
例如: session_id=abc123
'body': 从请求体中获取参数值(适用于原始请求体,如 XML 或自定义格式)。

parser.add_argument(name='test01', location='form', type=int, required=True, default=1, help='id必填字段',choices=("1", "2"))
parser.add_argument(name='test02', location='args', type=str)
parser.add_argument(name='test03',location='headers',type=bool)
parser.add_argument(name='test04',location='cookies',type=float)
parser.add_argument(name='test05', location='json', type=list,  required=False)

获取该输入参数
flask-restx方式获取：args = parser.parse_args()
flask获取：args = request.args
```

model = api.model() 类型

    ns = Namespace(name="用户管理", description='用户管理模块')
    parser = ns.model('CreateUserSchema', {
        'name': fields.String(required=True, description="用户名称"),
        'password': fields.String(required=True, description="用户密码"),
        'email': fields.String(required=True, description="联系邮箱"),
        'remark': fields.String(description="备注信息"),
    })
    获取该输入参数
    flask-restx方式获取：args = ns.payload
    flask获取：args = request.get_json()

### 使用说明

1. 创建`.env`文件

	```
	# .env file example
	
	FLASK_APP=api
	FLASK_CONFIG=development
	# Read more at https://github.com/theskumar/python-dotenv
	```

2. 启动虚拟环境

	```sh
	# 启动虚拟环境
	#on windows
	$ activate venv
	#on linux
	$ source activate venv
	```

3. 建立数据库、启动api

	```sh
	$ flask db init
	$ flask db migrate 
	$ flask db upgrade 
	
	# 启动api
	$ flask run

