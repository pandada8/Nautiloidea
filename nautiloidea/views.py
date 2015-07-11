from nautiloidea import app, need_login
from flask import request, render_template, session, jsonify, g, abort, make_response, send_from_directory, redirect
from . import model
from datetime import datetime
from uuid import uuid4 as uuid
import os

__folder__ = os.path.split(__file__)[0]

def update_position():
    @wraps(func)
    def wrappers(*args, **kwargs):
        if request.args.get('deviceid'):
            g.t = datetime.now().timestamp()
            device = model.Device.try_get(deviceid=deviceid)
            position = request.args.get('gps') or request.form.get('gps')
            if device:
                if position:
                    latitude, longtitude = position.split("|")
                    device.last_status['position'] = {"latitude": int(latitude), "longtitude": int(longtitude), "t": g.t}
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
            return jsonify(err=0, msg="登陆成功", user=user[0].user_info())
        else:
            return jsonify(err=1, msg="登录失败")


@app.route('/logout')
def logout_user():
    session.clear()
    return redirect('/')

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
        elif operation == 'erase':
            password = request.form.get('password')
            if g.users.check_pwd(password):
                to_send['operation'] = 'erase'
            else:
                abort(403)
        elif operation == 'lock':
            to_send['operation'] = 'lock'
        elif operation == 'get_file':
            to_send['operation'] = 'get_life'
            to_send['path'] = 'get_life'
        elif operation == "get_list":
            to_send['operation'] = 'get_list'
            if 'path' in request.form:
                to_send['path'] = request.form['path']
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
def device_online():
    deviceid = request.args['deviceid']  #TODO: MODIFY HERE
    device = model.Device.try_get(deviceid=deviceid)  #FIXME: Fill the position
    position = request.args.get('gps', '')
    if device:
        with model.db.transaction():
            now = datetime.now()
            device_record = model.DeviceRecords.create(event="online", device=device, time=now, position=position)
            device.last_status = device_record._to_dict()
            device.save()
        return jsonify(err=0)
    else:
        return jsonify(err=1, msg="No Such Device, You Should bind first")

@app.route('/offline')
def device_offline():
    deviceid = request.args['deviceid']
    device = model.Device.try_get(deviceid=deviceid)
    position = request.args.get('gps', '')
    if device:
        with model.db.transaction():
            now = datetime.now()
            device_record = model.DeviceRecords.create(event="offline", device=device, time=now, position=position)
            device.last_status = device_record._to_dict()
            device.save()
        return jsonify(err=0)
    else:
        return jsonify(err=1, msg="No Such Device, You Should bind first")

@app.route('/heartbeat')
def device_heartbeat():
    deviceid = request.args['deviceid']
    device = model.Device.try_get(deviceid=deviceid)
    position = request.args.get('gps', '')
    if device:
        with model.db.transaction():
            now = datetime.now()
            device_record = model.DeviceRecords.create(event="heartbeat", device=device, time=now, position=position)
            device.last_status = device_record._to_dict()
            device.save()
        return jsonify(err=0)
    else:
        return jsonify(err=1, msg="No Such Device, You Should bind first")

@app.route('/api/message')
def user_massage():
    msgs = []
    return jsonify(err=0, msg=msgs)

@app.route("/status")
@need_login()
def return_status():
    device_id = request.args['device']
    if device_id:
        device = model.Device.try_get(deviceid=device_id)
        if device and device.owner.id == g.user.id:
            return jsonify(err=0, status=device.last_status)
    return jsonify(err=1, msg="Oops")


@app.route('/bind', methods=["POST"])
@need_login()
def device_bind():
    deviceid = request.form['deviceid']
    phone_number = request.form.get("deviceName", '')
    if model.Device.try_get(deviceid=deviceid):
        return jsonify(err=1, msg="The devices is around bound, you should unbind it first")
    with model.db.transaction():
        device = model.Device.create(deviceid=deviceid, owner=g.user, last_status={}, phone_number=phone_number)
        g.user.devices.append(dict(deviceid=deviceid, phone_number=phone_number, id=device.id))
        g.user.save()
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
