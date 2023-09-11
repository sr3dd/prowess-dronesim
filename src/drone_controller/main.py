import os
import uuid

from fastapi import FastAPI
import requests

DRONE_HOST = os.environ['DRONE_HOST']
DRONE_PORT = os.environ['DRONE_PORT']

AC_HOST = os.environ['AC_HOST']
AC_PORT = os.environ['AC_PORT']

dc_id = uuid.uuid4().hex

app = FastAPI()

@app.get("/id")
def return_id():
    print('ID requested from AC...')
    return {'id': dc_id}

@app.post("/init")
def move_drone(body):
    body['id'] = dc_id
    url = f'http://{DRONE_HOST}:{DRONE_PORT}/move'
    r = requests.post(url, json=body)
    return body

@app.post("/move")
def move_drone(body):
    url = f'http://{DRONE_HOST}:{DRONE_PORT}/move'
    r = requests.post(url, json=body)
    return body

@app.get("/kill")
def drone_invalid():
    print('Drone battery depleted.')
    url = f'http://{AC_HOST}:{AC_PORT}/droneupdate/{dc_id}'

    r = requests.get(url)

    return url
