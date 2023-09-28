import os
import uuid

from fastapi import FastAPI
from pydantic import BaseModel
import requests

DRONE_HOST = os.environ['DRONE_HOST']
DRONE_PORT = os.environ['DRONE_PORT']

AC_HOST = os.environ['AC_HOST']
AC_PORT = os.environ['AC_PORT']

dc_id = uuid.uuid4().hex

app = FastAPI()

class Move(BaseModel):
    outx: int
    outy: int
    inx: int
    iny: int

@app.get("/id")
def return_id():
    print('ID requested from AC...')
    return {'id': dc_id}

@app.post("/init")
async def move_drone(move_data: Move):
    body = move_data.model_dump()
    body['dc_id'] = dc_id
    url = f'http://{DRONE_HOST}:{DRONE_PORT}/init'
    r = requests.post(url, json=body)
    return body

@app.post("/move")
async def move_drone(move_data: Move):
    url = f'http://{DRONE_HOST}:{DRONE_PORT}/move'
    r = requests.post(url, json=move_data.model_dump())
    return move_data

@app.get("/kill")
async def drone_invalid():
    print('Drone battery depleted.')
    url = f'http://{AC_HOST}:{AC_PORT}/droneupdate/{dc_id}'
    r = requests.get(url)
    return url
