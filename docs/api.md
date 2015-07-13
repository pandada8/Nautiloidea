

## 用户注册

调用URL:

    http://127.0.0.1:5000/signup

调用示例:

    POST http://127.0.0.1:5000/signup

Params:

    {}

Data:

    {'email': 'test@test.com', 'password': 'testpwd', 'username': 'Test'}

返回数据实例:

    {'err': 0, 'msg': '成功注册'}


## 用户登录（使用用户名）

调用URL:

    http://127.0.0.1:5000/signin

调用示例:

    POST http://127.0.0.1:5000/signin

Params:

    {}

Data:

    {'password': 'testpwd', 'username': 'Test'}

返回数据实例:

    {'err': 0,
     'msg': '登陆成功',
     'user': {'devices': [],
              'email': 'test@test.com',
              'uid': 1,
              'username': 'Test'}}


## 绑定设备

调用URL:

    http://127.0.0.1:5000/bind

调用示例:

    POST http://127.0.0.1:5000/bind

Params:

    {}

Data:

    {'deviceName': 'China Mobile', 'deviceid': 'device1'}

返回数据实例:

    {'err': 0, 'msg': 'bind success'}


## 发送心跳包

调用URL:

    http://127.0.0.1:5000/heartbeat

调用示例:

    GET http://127.0.0.1:5000/heartbeat?latitude=1.233&longitude=1.234&deviceid=device1

Params:

    {'deviceid': 'device1', 'latitude': '1.233', 'longitude': '1.234'}

Data:

    {}

返回数据实例:

    {'err': 0}


## 用户登录（使用邮箱）

调用URL:

    http://127.0.0.1:5000/signin

调用示例:

    POST http://127.0.0.1:5000/signin

Params:

    {}

Data:

    {'password': 'testpwd', 'username': 'test@test.com'}

返回数据实例:

    {'err': 0,
     'msg': '登陆成功',
     'user': {'devices': [{'deviceName': 'China Mobile',
                           'deviceid': 'device1',
                           'id': 1,
                           'last_status': {},
                           'owner': 1}],
              'email': 'test@test.com',
              'uid': 1,
              'username': 'Test'}}


## 绑定无昵称的设备

调用URL:

    http://127.0.0.1:5000/bind

调用示例:

    POST http://127.0.0.1:5000/bind

Params:

    {}

Data:

    {'deviceid': 'device2'}

返回数据实例:

    {'err': 0, 'msg': 'bind success'}


