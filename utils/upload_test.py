import requests

r = requests.session()
username = 'Test'
password = "testpwd"
print(r.post("http://127.0.0.1:5000/signin", data={"username": username, "password": password}).json())
print(r.get("http://127.0.0.1:5000/heartbeat", params={"latitude": 123.44, "longtitude": 34.2}).json())
# Received something like 
# {"operaition": "get_list"}
r.post("http://127.0.0.1:5000/filelist_callback", data={})