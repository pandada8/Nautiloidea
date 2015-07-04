from nautiloidea import app, model
from flask.ext.script import Manager
import os
import getpass

manager = Manager(app)

@manager.command
def init():
    if not app.config['DEBUG']:
        print('请使用 PostgreSQL 的 createdb 创建数据库')
        input("创建完成后回车")
    model.init_db()
    print('创建上传目录')
    os.makedirs(app.config['UPLOAD'], exist_ok=True)

@manager.command
def admin_create():
    while True:
        username = input('Username: ')
        if username and not model.User.try_get(username=username):
            break
        else:
            print('Wrong input, retry')
    while True:
        email = input('Email: ')
        if email and not model.User.try_get(email=email):
            break
        else:
            print('Wrong input, retry')

    password = getpass.getpass()
    user = model.User()
    user.email = email
    user.username = username
    user.set_pwd(password)
    user.save()
    print("Create user successfully.")