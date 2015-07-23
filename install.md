# Install Guide

1. 首先确保电脑上有最新的`python3.4`和`node`环境
2. 使用`npm`安装`bower`(安装过可跳过这一步)
3. 在 `nautiloidea/static` 目录下执行 `bower install`
4. 执行 `npm install`
5. 执行 `gulp`
6. 回到原来的目录安装 Python 依赖，`pip install -r requirements.txt` (如果可以的话可以用`virtualenv`做隔离)
7. 修改 `config.py`,加入自己的Key等信息
8. （如果使用了virtualenv请激活），执行 `python manage.py init` 初始化
10. 使用`python manage.py runserver` 启动 web 服务
11. 使用`python manage.py run_sender` 启动发送服务

# Tips

* 使用`*_PROXY`等环境变量来解决网络环境不好的问题
*
