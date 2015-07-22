import os

secret_key = b'\x8d3\xf9\xd9f\xd7B\xa6\xb5ec\xe1\xf62g&wh\\xae\xed\xa4D\xbd^\xa8\x16\x9e\x1a\x18dt\xd9=\xa8\xd4\xc9 \xb6\x19'
app_id = 2100130300
app_secret = "bcd24dab3c8711033901b672635ef465"

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
