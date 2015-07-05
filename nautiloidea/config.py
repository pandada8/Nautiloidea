import os


class DevSetting:
    UPLOAD = os.path.normpath(os.path.join(os.path.split(__file__)[0], '../upload'))
    DEBUG = True

class ProcutionSetting:
    pass