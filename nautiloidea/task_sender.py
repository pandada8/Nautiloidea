"""
fetch the queued task in the datebase and send them to the Tencent API
"""
import aiohttp
import asyncio
from . import model
from datetime import datetime
import time
import threading
import logging
import json
import hashlib
from . import app

appid = app.config['TENCENT_APPID']
token = app.config['TENCENT_TOKEN']

if app.debug:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

def fetchUnFinished():
    query = model.OperationQueue.select().where(model.OperationQueue.sent == False).order_by(model.OperationQueue.id.desc()).limit(1).execute()
    result = list(query)
    if result:
        return result[0]
    else:
        return None

def md5(s):
    return hashlib.md5sum(s.encode("UTF8")).hexdigest()

@asyncio.coroutine
def send_task(data):
    target_device = data.deviceid
    params = {
        "device_token": data.target_device.deviceid,
        "message_type": 2,
        "message": json.dumps({'content':data.operation ,'title': 'none', "custom_content": {'task_id': data.id}}, ensure_ascii=False),
        "timestamp": int(time.time()),
        "access_id": appid,
        "expire_time": 86400,
    }
    sign = "POSTopenapi.xg.qq.com/v2/push/single_device{}{}".format(''.join([str(i)+"="+str(j) for i,j in sorted(params.items(), key=lambda x:x[0])]), token)
    print(sign, md5(sign))
    params['sign'] = md5(sign)
    response = yield from aiohttp.get('http://openapi.xg.qq.com/v2/push/single_device', params=params)
    content = json.loads((yield from response.read()).decode())
    print(content)
    if content['ret_code']:
        data.msg['err'] = content['err_msg']
        logging.warn('Error', content['err_msg'])
    return




@asyncio.coroutine
def run():
    while True:
        data = fetchUnFinished()
        if data:
            result = yield from send_task(data)
            data.sent = True
            data.save()
        else:
            yield from asyncio.sleep(1)
def run_thread():
    event_loop = asyncio.get_event_loop()
    event_loop.run_until_complete(run())

def run_in_thread():
    thread = threading.Thead(target=run_thread)
    thread.start()
    return thread
