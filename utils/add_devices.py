import requests

r = requests.session()
r.post("http://127.0.0.1:5000/signin", data={"username": 'pandada8', 'password': "pandada8"})
r.post("http://127.0.0.1:5000/bind", data={"deviceid": "jsdkkdjskd", 'phone_number': "123787788"})
