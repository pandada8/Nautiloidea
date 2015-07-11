import os

secret_key = b'`\xcf\x89}HC\x97\x1b\xe10\x06@\xee\xf3#\x9c\xaf\x90g\xe2X\x11;QrI\xc0\x0b\xc0\x8d\xcfOX+\xa4\xadj\xe9\x9c\xf9'
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
