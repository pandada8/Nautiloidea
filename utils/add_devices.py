import requests

r = requests.session()
r.post("http://127.0.0.1:5000/signin", data={"username": 'pandada8', 'password': "pandada8"})
r.post("http://127.0.0.1:5000/bind", data={"deviceid": "jsdkkdjskd", 'phone_number': "1290301923"})
r.post("http://127.0.0.1:5000/bind", data={"deviceid": "jdaslfkjslkdj", 'phone_number': "1293-1902-39"})
