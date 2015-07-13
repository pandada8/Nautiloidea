

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
              'uid': 8,
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

    GET http://127.0.0.1:5000/heartbeat?latitude=1.233&deviceid=device1&longitude=1.234

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
     'user': {'devices': [{'deviceid': 'device1',
                           'id': 9,
                           'last_status': {'position': {'latitude': 1.233,
                                                        'longtitude': 1.234,
                                                        't': 1436797265.975038},
                                           'record': {'device': 9,
                                                      'event': 'heartbeat',
                                                      'id': 8,
                                                      'position': {'latitude': 1.233,
                                                                   'longtitude': 1.234,
                                                                   't': 1436797265.975038},
                                                      'time': 1436797265.979786}},
                           'owner': 8,
                           'phone_number': 'China Mobile'}],
              'email': 'test@test.com',
              'uid': 8,
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


