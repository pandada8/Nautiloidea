import requests
import random
from functools import wraps
import string
import sys
from jinja2 import Template

DOCTEMP = '''
{% for i in apis %}
## {{i.text}}

调用URL:

    {{i.origin_url}}

调用示例:

    {{i.method}} {{i.ret.request.url}}

Params:

{{i.params | pprint | indent(indentfirst=True)}}

Data:

{{i.data | pprint | indent(indentfirst=True)}}

返回数据实例:

{{ i.ret.json() | pprint | indent(indentfirst=True)}}

{% endfor %}
'''


def randomString(length=10):
    return "".join([random.choice(string.ascii_letters) for i in range(length)])

apis = []
r = requests.session()


def clean_session():
    global r
    r = requests.session()


def show_debug_info(method, url, params, data, text):
    """
    This is a helper function based on requests api to send api requests and
    generate api documents
    """
    print("Start testing the {}:".format(url), file=sys.stderr)
    ret = r.request(method, url, params=params, data=data)
    apis.append({
        "ret": ret,
        "method": method,
        "params": params,
        "data": data,
        "origin_url": url,
        "text": text
    })
    print("Finish testing the {}:".format(url), file=sys.stderr)


def gen_the_docs():
    doc = Template(DOCTEMP)
    return doc.render(apis=apis)

username = "Test"
password = "testpwd"
deviceid = "device1"
deviceid2 = "device2"
email = "test@test.com"
r = requests.session()

show_debug_info("POST", "http://127.0.0.1:5000/signup", {}, {"username": username, 'password': password, "email": email}, "用户注册")
clean_session()
show_debug_info("POST", "http://127.0.0.1:5000/signin", {}, {"username": username, "password": password}, "用户登录（使用用户名）")
show_debug_info("POST", "http://127.0.0.1:5000/bind", {}, {"deviceName": "China Mobile", "deviceid": deviceid}, "绑定设备")
show_debug_info("GET", "http://127.0.0.1:5000/heartbeat", {"latitude": "1.233", "longitude": "1.234", "deviceid": deviceid}, {}, "发送心跳包")
clean_session()
show_debug_info("POST", "http://127.0.0.1:5000/signin", {}, {"username": email, "password": password}, "用户登录（使用邮箱）")
show_debug_info("POST", "http://127.0.0.1:5000/bind", {}, {"deviceid": deviceid2}, "绑定无昵称的设备")


print(gen_the_docs())
