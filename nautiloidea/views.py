from nautiloidea import app
from flask import request, render_template, session, jsonify
from . import model
from datetime import datetime


@app.route('/register', methods=["POST", "GET"])
def register_users():
    if request.method == 'GET':
        return render_template("register.html")
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        if model.User.select().where((model.User.username == username) | (model.User.email == email)).count() > 0:
            return jsonify(err=1, msg="该用户名或邮箱已被注册")
        else:
            user = model.User()
            user.username = username
            user.email = email
            user.set_pwd(password)
            user.save()
            return jsonify(err=0, msg="成功注册")

@app.route('/login', methods=["POST", "GET"])
def login_user():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = model.User.select().where((model.User.username == username) | (model.User.email == email)).limit(1).execute()
        if user and user.check_pwd(password):
            # login the user
            session['user'] = user.id
            return jsonify(err=0, msg="登陆成功")
        else:
            return jsonify(err=1, msg="登录失败")


@app.route('/online'):
def device_online():
    deviceid = request.args['deviceid']  #TODO: MODIFY HERE
    device = model.Device.try_get(deviceid=deviceid)
    if device:
        now = datetime.now()
        model.DeviceRecords.create(action="online", device=device, )


    else:
        return jsonify(err=1, msg="No Such Device, You Should bind first")


