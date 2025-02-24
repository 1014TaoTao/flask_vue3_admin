# 基础镜像
FROM python:3.10
# 镜像作者
MAINTAINER 管理员
# 设置 python 环境变量
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
# 设置时区
ENV TZ Asia/Shanghai
# 更新pip
RUN pip install -U pip
# 设置国内镜像源
RUN pip config set global.index-url http://mirrors.aliyun.com/pypi/simple
RUN pip config set install.trusted-host mirrors.aliyun.com
# 升级pip版本
RUN python -m pip install --upgrade pip
# 安装工具
RUN pip install setuptools
# 创建容器工作目录
RUN mkdir -p /data/flask_restx_project
# 设置容器内工作目录
WORKDIR /data/flask_restx_project
# 将当前主机目录全部文件复制至容器工作目录
COPY . /data/flask_restx_project
# 安装离线包目录
RUN pip install Flask-Script-2.0.6/

# 安装依赖
RUN pip install -r requirements.txt
RUN pip install uwsgi

RUN apt-get update ##[edited]
RUN apt-get install ffmpeg libsm6 libxext6 nginx -y

RUN pip install -r requirements.txt

# 部署 nginx
RUN rm /etc/nginx/sites-enabled/default
COPY nginx_flask.conf /etc/nginx/sites-available/
RUN ln -s /etc/nginx/sites-available/nginx_flask.conf /etc/nginx/sites-enabled/nginx_flask.conf
RUN echo "daemon off;" >> /etc/nginx/nginx.conf

#CMD 运行以下命令，daemon off后台运行，否则启动完就自动关闭
CMD ["nginx", "-g","daemon off;"]  

ENTRYPOINT ["gunicorn", "--config", "gunicorn.py", "api:app"]