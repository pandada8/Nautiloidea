from flask import Flask, g, session, abort
from json import JSONEncoder, JSONDecoder
from datetime import datetime
import os
from functools import wraps
from . import config
import logging

app = Flask(__name__)
if os.environ.get('debug') or os.environ.get('DEBUG'):
    logging.basicConfig(level=logging.DEBUG)
    app.logger.info('Running in debug mode')
    app.config.from_object(config.DevSetting)
    app.debug = True
    app.secret_key = "123456"
else:
    app.config.from_object(config.ProcutionSetting)
    app.secret_key = os.urandom(40)

class DateTimeJsonEncoder(JSONEncoder):

    def default(self, obj):
        try:
            if isinstance(obj, datetime):
                return obj.timestamp()
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)

app.json_encoder = DateTimeJsonEncoder

from . import model

@app.before_request
def hook_users():
    if session.get('user') is not None:
        g.user = model.User.try_get(id=int(session['user']))
        # print(g.user)
    else:
        g.user = None

def need_login(admin=False):
    def return_wrapper(func):
        @wraps(func)
        def wrappers(*args, **kwargs):
            if not g.user:
                abort(403)
            if admin and not g.user.super:
                abort(403)
            return func(*args, **kwargs)
        return wrappers
    return return_wrapper

from . import views
