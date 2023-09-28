import os
import time

from fastapi import BackgroundTasks, FastAPI
from pydantic import BaseModel
import requests

AC_HOST = os.environ['AC_HOST']
AC_PORT = os.environ['AC_PORT']

INFERENCE_TIME = int(os.environ['INFERENCE_TIME'])

class Sample(BaseModel):
    outx: int
    outy: int
    inx: int
    iny: int
    dc_id: str

app = FastAPI()

def notify_auto_controller(notification: Sample):
    url = f'http://{AC_HOST}:{AC_PORT}/inference/{notification.dc_id}'
    #a = notification.model_dump_json()
    r = requests.get(url)

@app.post("/infer")
async def infer_data(body: Sample, background_tasks: BackgroundTasks):
    print(f'Received data sample from drone...')
    time.sleep(INFERENCE_TIME)

    background_tasks.add_task(notify_auto_controller, body)
    print(f'Update auto-controller of inference from drone: {body.dc_id}')
    