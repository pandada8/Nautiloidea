from peewee import Model, SqliteDatabase, PostgresqlDatabase, CharField, BooleanField, ForeignKeyField, DateTimeField, TextField
from nautiloidea import app
import os
import random
import string
import hashlib
import json
from datetime import datetime, timedelta

if app.debug:
    db = SqliteDatabase(os.path.normpath(os.path.join(os.path.split(__file__)[0], '../data.sqlite3')))
else:
    db = PostgresqlDatabase()  # TODO: Using the config the config the password and user

def randomSalt(length=20):
    return "".join([random.choice(string.printable[:-5]) for i in range(length)])

def encrypt(password, salt):
    salt_ = hashlib.sha384(salt.encode('UTF-8')).hexdigest()
    return hashlib.sha256(password.encode('UTF-8') + salt + salt_).hexdigest()

class BaseModel(Model):

    @classmethod
    def try_get(cls, **kwargs):
        try:
            return cls.get(**kwargs)
        except cls.DoesNotExist:
            return kwargs['default'] if 'default' in kwargs else None

    def _to_dict(self):
        return self._data

    class Meta:
        database = db

class JSONField(TextField):

    def python_value(self, value):
        try:
            return json.loads(value)
        except Exception as e:
            app.logger.exception(e)
            return {}

    def db_value(self, value):
        return json.dumps(value)


class User(BaseModel):

    username = CharField(unique=True)
    password = CharField(max_length=64)
    salt = CharField(max_length=64)
    email = CharField(unique=True)
    super = BooleanField(default=False)  # the admin account
    devices = JSONField(default={})

    def set_pwd(self, password):
        self.salt = randomSalt(64)
        self.password = encrypt(password, self.salt)

    def check_pwd(self, password):
        return encrypt(password, self.salt) == self.password

    def user_info(self):
        return {
            'username': self.username,
            'uid': self.id,
            'email': self.email
        }

class Device(BaseModel):
    deviceid = CharField(max_length=256)
    last_status = JSONField(default={})
    owner = ForeignKeyField(User, null=True)

    def online(self):
        now = datetime.now().timestamp()
        if not self.last_status:
            return False
        if now - self.last_status['time'] > 3 * 60:
            return False
        if self.last_status['event'] == 'offline':
            return False
        if self.last_status['event'] == 'online' or self.last_status['event'] == 'heartbeat':
            return True

class DeviceRecords(BaseModel):
    device = ForeignKeyField(Device)
    time = DateTimeField()
    position = TextField(null=True)
    action = CharField()  # online or heartbeat
    event = CharField()  # online or heartbeat

class OperationQueue(BaseModel):
    target_device = ForeignKeyField(Device)
    operation = JSONField(default={})
    created = DateTimeField()
    recv_time = DateTimeField(null=True)

def init_db():
    db.create_tables([User, DeviceRecords, Device, OperationQueue], safe=True)



