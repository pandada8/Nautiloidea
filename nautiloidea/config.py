import os

secret_key = b'`\xcf\x89}HC\x97\x1b\xe10\x06@\xee\xf3#\x9c\xaf\x90g\xe2X\x11;QrI\xc0\x0b\xc0\x8d\xcfOX+\xa4\xadj\xe9\x9c\xf9'

class DevSetting:
    UPLOAD = os.path.normpath(os.path.join(os.path.split(__file__)[0], '../upload'))
    DEBUG = True
    secret_key = secret_key

class ProcutionSetting:
    pass