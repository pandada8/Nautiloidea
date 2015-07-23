import os

secret_key = '<RandomText>'
app_id = 12345 # <your app id>
app_secret = "secret" #<Your app secret>

class DevSetting:
    UPLOAD = os.path.normpath(os.path.join(os.path.split(__file__)[0], '../upload'))
    DEBUG = True
    SECRET_KEY = secret_key
    TENCENT_APPID = app_id
    TENCENT_TOKEN = app_secret


class ProcutionSetting:
    SECRET_KEY = secret_key
    TENCENT_APPID = app_id
    TENCENT_TOKEN = app_secret
    DEBUG = False
    UPLOAD = os.path.normpath(os.path.join(os.path.split(__file__)[0], '../upload'))
