from nautiloidea import app, need_login
from flask import request, render_template, session, jsonify, g, abort, make_response, send_from_directory, redirect
from . import model
from datetime import datetime
from uuid import uuid4 as uuid
import os
from functools import wraps
import json

__folder__ = os.path.split(__file__)[0]


def update_position(func):
    @wraps(func)
    def wrappers(*args, **kwargs):
        if request.args.get('deviceid'):
            g.now = datetime.now()
            g.t = g.now.timestamp()
            g.device = model.Device.try_get(deviceid=request.args.get('deviceid'))
            position = request.args.get('latitude')
            if g.device:
                if position:
                    latitude, longtitude = request.args['latitude'], request.args['longitude']
                    g.position = {"latitude": float(latitude), "longtitude": float(longtitude), "t": g.t}
                    g.device.last_status['position'] = g.position
                else:
                    g.position = {}
                return func(*args, **kwargs)
            else:
                abort(403)
        else:
            abort(400)
    return wrappers


@app.route('/')
def index_page():
    return send_from_directory(os.path.join(__folder__, 'static'), 'index.html')


@app.route('/user')
@need_login()
def user_index():
    return render_template('user.html', data=g.user.user_info())


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
            session['user'] = user.id
            return jsonify(err=0, msg="成功注册")


@app.route('/signin', methods=["POST", "GET"])
def login_user():
    if request.method == "GET":
        if g.user:
            return redirect('/user')
        else:
            return render_template("login.html")
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = list(model.User.select().where((model.User.username == username) | (model.User.email == username)).limit(1).execute())
        if user and user[0].check_pwd(password):
            # login the user
            session['user'] = user[0].id
            print(user[0].user_info())
            return jsonify(err=0, msg="登陆成功", user=user[0].user_info())
        else:
            return jsonify(err=1, msg="登录失败")


@app.route('/logout')
def logout_user():
    session.clear()
    return redirect('/')


def check_password():
    password = request.form.get('password')
    if not g.user.check_pwd(password):
        abort(403)


@app.route("/operation", methods=['GET', 'POST'])
def save_operation():
    if request.method == 'GET':
        return jsonify(err=1, msg="Not Implemented")
    elif request.method == 'POST':
        operation = request.form.get('operation')
        device_id = request.form['deviceid']
        to_send = {}

        if operation == 'alarm':
            to_send['operation'] = 'alarm'
        elif operation == 'disalarm':
            to_send['operation'] = 'disalarm'
        elif operation == 'erase':
            check_password()
            to_send['operation'] = 'erase'
        elif operation == 'lock':
            to_send['operation'] = 'lock'
        elif operation == 'unlock':
            check_password()
            to_send['operation'] = 'unlock'
        elif operation == 'get_file':
            to_send['operation'] = 'get_file'
            to_send['path'] = request.form['path']
        elif operation == "get_list":
            to_send['operation'] = 'get_list'
            # if 'path' in request.form:
            #     to_send['path'] = request.form['path']
        else:
            print(operation)
            abort(400)
        with model.db.transaction():
            device = model.Device.try_get(deviceid=device_id)
            now = datetime.now()
            print(device, device.owner.id, g.user.id)
            if device and device.owner.id == g.user.id:
                model.OperationQueue.create(
                    target_device=device,
                    operation=to_send,
                    created=now,
                    operation_type=to_send['operation'],
                )
            else:
                abort(400)
        return jsonify(err=0, msg="操作成功")


@app.route('/online')
@update_position
def device_online():
    with model.db.transaction():
        device_record = model.DeviceRecords.create(event="online", device=g.device, time=g.t, position=g.position)
        g.device.last_status['status'] = device_record._to_dict()
        g.device.save()
    return jsonify(err=0)


@app.route('/offline')
def device_offline():
    with model.db.transaction():
        device_record = model.DeviceRecords.create(event="offline", device=g.device, time=g.t, position=g.position)
        g.device.last_status['status'] = device_record._to_dict()
        g.device.save()
    return jsonify(err=0)


@app.route('/heartbeat')
@update_position
def device_heartbeat():
    with model.db.transaction():
        device_record = model.DeviceRecords.create(event="heartbeat", device=g.device, time=g.t, position=g.position)
        g.device.last_status['status'] = device_record._to_dict()
        g.device.save()
    return jsonify(err=0)


@app.route("/status")
@need_login()
def return_status():
    device_id = request.args['device']
    if device_id:
        device = model.Device.try_get(deviceid=device_id)
        uploaded = [i._to_dict() for i in model.UploadedFile.select().where(model.UploadedFile.device == device)]
        if device and device.owner.id == g.user.id:
            return jsonify(err=0, status=device.last_status, files=device.files, uploaded=uploaded)  # TODO: send user the information
    return jsonify(err=1, msg="Oops")


@app.route('/bind', methods=["POST"])
@need_login()
def device_bind():
    deviceid = request.form['deviceid']
    deviceName = request.form.get("deviceName")
    if model.Device.try_get(deviceid=deviceid):
        return jsonify(err=1, msg="The devices is around bound, you should unbind it first")
    with model.db.transaction():
        device = model.Device.create(deviceid=deviceid, owner=g.user, last_status={}, deviceName=deviceName)
        g.user.devices.append(dict(deviceid=deviceid, deviceName=deviceName, id=device.id))
        g.user.save()
    return jsonify(err=0, msg='bind success')


@app.route('/callback/fileupload', methods=["POST"])
@update_position
def device_upload():
    operation_id = int(request.args.get("task_id"))
    user = g.device.owner
    task = model.OperationQueue.try_get(id=operation_id)
    print(request.form, request.files)
    if task:
        origin_path = request.form['path']
        fid = str(uuid())
        saved_path = "{}/{}/{}".format(g.now.year, g.now.month, fid)
        os.makedirs(os.path.join(app.config["UPLOAD"], os.path.split(saved_path)[0]), exist_ok=True)
        list(request.files.values())[0].save(os.path.join(app.config["UPLOAD"], saved_path))

        model.UploadedFile.create(user=user, device=g.device, origin_path=origin_path, saved_path=saved_path, file_id=fid, time=g.now)

        return jsonify(ret=0, msg="OK")
    else:
        abort(400)


@app.route("/callback/filelist", methods=["POST"])
@update_position
def device_filelist():
    operation_id = int(request.args.get("task_id"))
    print(operation_id)
    task = model.OperationQueue.try_get(id=operation_id)
    print('task')
    if task:
        with model.db.transaction():

            now = datetime.now()
            # data = request.get_json(force=True)
            print(request.form)
            data = request.form['fileList']
            data = json.loads(data)
            task.responsed = now
            task.save()

            g.device.files = {'data': data, "time": now}
            g.device.save()

        return jsonify(err=0, msg="保存成功")
    else:
        abort(400)


@app.route('/f/<file_id>')
@need_login()
def get_file(file_id):
    file = model.UploadedFile.try_get(file_id=file_id)
    if file and file.user.id == g.user.id:
        print(file, file.user.id)
        if app.debug:
            return send_from_directory(app.config['UPLOAD'], file.saved_path,  as_attachment=True, attachment_filename=os.path.split(file.origin_path)[-1])
        else:
            response = make_response()
            response.headers['Content-Type'] = ''
            response.headers['X-Accel-Redirect'] = file.saved_path  # TODO write a nginx config to fix the url
            return response
    else:
        abort(404)
