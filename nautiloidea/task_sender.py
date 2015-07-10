"""
fetch the queued task in the datebase and send them to the Tencent API
"""
import aiohttp
import asyncio
from . import model
from datetime import datetime
import threading
import logging
from . import app

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

def send_task(data):
    pass

@asyncio.coroutine
def run():
    while True:
        data = fetchUnFinished()
        if data:
            result = yield from send_task(data._to_dict())
            data.sent = True
            data.msg = result
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
