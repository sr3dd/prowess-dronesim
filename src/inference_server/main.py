import os
import time

from fastapi import FastAPI
import requests

AC_HOST = os.environ['AC_HOST']
AC_PORT = os.environ['AC_PORT']

INFERENCE_TIME = int(os.environ['INFERENCE_TIME'])

app = FastAPI()

@app.post("/infer/")
async def infer_data(body):
    
    print(f'Received data sample from drone...')
    time.sleep(INFERENCE_TIME)

    payload = {'id': body['id'], 'out_x': body['outx'], 'out_y': body['outy'],
                'in_x': body['inx'], 'in_y': body['iny']}
    
    url = f'http://{AC_HOST}:{AC_PORT}/inferenceupdate'

    r = requests.post(url, json=payload)

    return payload
