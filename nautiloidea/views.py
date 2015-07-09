from nautiloidea import app, need_login
from flask import request, render_template, session, jsonify, g, abort, make_response, send_from_directory
from . import model
from datetime import datetime
from uuid import uuid4 as uuid
import os

__folder__ = os.path.split(__file__)[0]

@app.route('/')
def index_page():
    return send_from_directory(os.path.join(__folder__, 'static'), 'index.html')


@app.route('/signup', methods=["POST", "GET"])
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


@app.route('/signin', methods=["POST", "GET"])
def login_user():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = list(model.User.select().where((model.User.username == username) | (model.User.email == username)).limit(1).execute())
        if user and user[0].check_pwd(password):
            # login the user
            session['user'] = user[0].id
            return jsonify(err=0, msg="登陆成功")
        else:
            return jsonify(err=1, msg="登录失败")


@app.route('/user')
@need_login()
def user_index():
    return render_template('user.html', data=g.user.user_info())

@app.route('/online')
def device_online():
    deviceid = request.args['deviceid']  #TODO: MODIFY HERE
    device = model.Device.try_get(deviceid=deviceid)  #FIXME: Fill the position
    if device:
        with model.db.transaction():
            now = datetime.now()
            device_record = model.DeviceRecords.create(event="online", device=device, time=now, position="")
            device.last_status = device_record._to_dict()
            device.save()
        return jsonify(err=0)
    else:
        return jsonify(err=1, msg="No Such Device, You Should bind first")

@app.route('/offline')
def device_offline():
    deviceid = request.args['deviceid']
    device = model.Device.try_get(deviceid=deviceid)
    if device:
        with model.db.transaction():
            now = datetime.now()
            device_record = model.DeviceRecords.create(event="offline", device=device, time=now, position="")
            device.last_status = device_record._to_dict()
            device.save()
        return jsonify(err=0)
    else:
        return jsonify(err=1, msg="No Such Device, You Should bind first")

@app.route('/heartbeat')
def device_heartbeat():
    deviceid = request.args['deviceid']
    device = model.Device.try_get(deviceid=deviceid)
    if device:
        with model.db.transaction():
            now = datetime.now()
            device_record = model.DeviceRecords.create(event="heartbeat", device=device, time=now, position="")
            device.last_status = device_record._to_dict()
            device.save()
        return jsonify(err=0)
    else:
        return jsonify(err=1, msg="No Such Device, You Should bind first")

@app.route('/bind')
@need_login()
def device_bind():
    deviceid = request.form['deviceid']
    if model.Device.try_get(deviceid=deviceid):
        return jsonify(err=1, msg="The devices is around bound, you should unbind it first")
    device = model.Device.create(deviceid=deviceid, owner=g.user, last_status={})
    return jsonify(err=0, msg='bind success')

@app.route('/upload')
def device_upload():
    deviceid = request.args['deviceid']
    now = datetime.now()
    device = model.Device.try_get(deviceid=deviceid)
    user = device.user
    if not device:
        abort(403)
    target_file_path = request.form['path']
    filename = uuid()
    saved_path = "{}/{}/{}".format(now.year, now.month, filename)
    os.makedirs(os.path.join(app.config['UPLOAD'], os.path.split(saved_path)[0]), exist_ok=True)
    request.files[0].save(os.path.join(saved_path))


@app.route('/f/<int:file_id>')
@need_login()
def get_file(file_id):
    file = model.try_get(id=file_id)
    if file and file.user.id == g.user.id:
        if app.debug:
            return send_from_directory(app.config['UPLOAD'], file.saved_path)
        else:
            response = make_response()
            response.headers['Content-Type'] = ''
            response.headers['X-Accel-Redirect'] = file.saved_path # TODO write a nginx config to fix the url
            return response
    else:
        abort(404)
