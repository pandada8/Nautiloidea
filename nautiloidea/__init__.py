from flask import Flask, g, session, abort
from json import JSONEncoder, JSONDecoder
from datetime import datetime
import os
from functools import wraps
from . import config
import logging

app = Flask(__name__)

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
app.secret_key = os.urandom(40)
if os.environ.get('debug') or os.environ.get('DEBUG'):
    logging.basicConfig(level=logging.DEBUG)
    app.logger.info('Running in debug mode')
    app.config.from_object(config.DevSetting)
else:
    app.config.from_object(config.ProcutionSetting)

from . import model

@app.before_request
def hook_users():
    if session.get('user'):
        g.user = model.User.try_get(id=int(session['user']))
    else:
        g.user = None

def need_login(admin=False):
    def return_wrapper(func):
        @wraps(func)
        def wrappers(*args, **kwargs):
            if g.user:
                if admin and g.user.super:
                    return func(*args, **kwargs)
                else:
                    abort(403)
                return func(*args, **kwargs)
            else:
                abort(403)
        return wrappers
    return return_wrapper

from . import views