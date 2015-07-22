import requests
import random
import string
import json
import pprint
import time


def randomText(length=4):
    return "".join([random.choice(string.ascii_letters) for i in range(length)])


r = requests.session()


def reset_session():
    global r
    r = requests.session()


username = "test_"
password = "Test_"
device = "test_"
email = "test_" "@test.com"
file_list = json.load(open("test.json"))


def show_debug_info(method, url, params, data, text, **kwargs):
    """
    This is a helper function based on requests api to send api requests and
    generate api documents
    """
    print("Start {} the {}:".format(method, url))
    print(text)
    print("Params: ")
    pprint.pprint(params)
    print("Data: ")
    pprint.pprint(data)
    ret = r.request(method, url, params=params, data=data, **kwargs)
    print("Return :")
    try:
        pprint.pprint(ret.json())
    except:
        print(ret.text)


show_debug_info("POST", "http://127.0.0.1:5000/signup", {}, {"username": username, 'password': password, "email": email}, "用户注册")
reset_session()
show_debug_info("POST", "http://127.0.0.1:5000/signin", {}, {"username": username, "password": password}, "用户登录（使用用户名）")
show_debug_info("POST", "http://127.0.0.1:5000/bind", {}, {"deviceName": "China Mobile", "deviceid": device}, "绑定设备")
show_debug_info("GET", "http://127.0.0.1:5000/heartbeat", {"latitude": "39.910", "longitude": "116.399", "deviceid": device}, {}, "发送心跳包")
try:
    for i in range(10):
        show_debug_info("GET", "http://127.0.0.1:5000/heartbeat", {"latitude": 39.910 + random.random(), "longitude": 116.399 + random.random(), "deviceid": device}, {}, "发送心跳包")
        #time.sleep(10)
except KeyboardInterrupt:
    pass
task_id = input("Task_id:")
show_debug_info("POST", "http://127.0.0.1:5000/callback/filelist", {"deviceid": device, "task_id": task_id}, json.dumps(file_list), "上传数据")
task_id = input("Task_id:")
file_path = input("file_path:")
show_debug_info("POST", "http://127.0.0.1:5000/callback/fileupload", {"deviceid": device, "task_id": task_id}, {"path":file_path}, "上传文件", files={"upload": open("test.json")})
