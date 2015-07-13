from nautiloidea import app, model
from flask.ext.script import Manager
import os
import getpass
import re

manager = Manager(app)

@manager.command
def init():
    if not app.config['DEBUG']:
        print('请使用 PostgreSQL 的 createdb 创建数据库')
        input("创建完成后回车")
        print("正在初始化数据库表")
        model.init_db()
    else:
        print("正在初始化数据库表")
        model.init_db()

    # print('初始化Secret Key')
    # with open('nautiloidea/config.py') as fp:
    #     content = fp.read()
    #     content = re.sub(r'^secret_key \= [\s\S]+?$', "secret_key = {}".format(repr(os.urandom(40))), content, flags=re.MULTILINE)
    # with open('nautiloidea/config.py', 'w') as fp:
    #     fp.write(content)

    print('创建上传目录')
    os.makedirs(app.config['UPLOAD'], exist_ok=True)


@manager.command
def admin_create():
    while True:
        username = input('Username: ')
        if username and not model.User.try_get(username=username):
            break
        else:
            print('Existed, retry')
    while True:
        email = input('Email: ')
        if email and not model.User.try_get(email=email):
            break
        else:
            print('Existed, retry')

    password = getpass.getpass()
    user = model.User()
    user.email = email
    user.username = username
    user.set_pwd(password)
    user.save()
    print("Create user successfully.")

@manager.command
def run_sender():
    from nautiloidea.task_sender import run_in_thread
    run_in_thread()

if __name__ == '__main__':
    manager.run()
