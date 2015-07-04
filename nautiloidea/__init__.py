from flask import Flask, g, session
from json import JSONEncoder, JSONDecoder
from datetime import datetime
import os

app = Flask(__name__)

class DateTimeJsonEncoder(JSONEncoder):

    def default(self, obj):
        try:
            if isinstance(obj, datetime):
                return obj.isoformat() + "+0800"
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)

app.json_encoder = DateTimeJsonEncoder
app.secret_key = os.urandom(40)

from . import model
from . import views

@app.before_request()
def hook_users():
    if session['user']:
        model.
