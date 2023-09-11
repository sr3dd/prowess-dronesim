from itertools import product
import os
import random
import time

from fastapi import FastAPI
from pydantic import BaseModel
import requests

random.seed(10)

CONTROLLER_HOSTS = os.environ['CONTROLLER_HOSTS'].split('|')
CONTROLLER_PORT = os.environ['CONTROLLER_PORT']
OUTER_GRID = int(os.environ['OUTER_GRID'])
INNER_GRID = int(os.environ['INNER_GRID'])

all_grid_blocks = list(product(range(OUTER_GRID), range(OUTER_GRID), range(INNER_GRID), range(INNER_GRID)))

dc_hosts = [{'host': i, 
             'host_id': None, 
             'port': CONTROLLER_PORT, 
             'status': 'Available'} for i in CONTROLLER_HOSTS]

def init_dc_hosts():
    for dc_host in dc_hosts:
        url = f'http://{dc_host["host"]}:{dc_host["port"]}/id'
        response = requests.get(url)
        if response.ok:
            dc_host['host_id'] = response.json()['id']
        else:
            print(f'No response from drone controller: {dc_host["host"]}')
            dc_host['status'] == 'Unavailable'

def get_grid():
    grid_index = random.randrange(len(all_grid_blocks))
    return all_grid_blocks.pop(grid_index)

def init_drone(dc_host, grid_position):
    url = f'http://{dc_host["host"]}:{dc_host["port"]}/init'
    payload = {'outx': grid_position[0], 'outy': grid_position[1],
               'inx': grid_position[2], 'iny': grid_position[3]}
    r = requests.post(url, json=payload)

def move_drone(dc_host, grid_position):
    url = f'http://{dc_host["host"]}:{dc_host["port"]}/init'
    payload = {'outx': grid_position[0], 'outy': grid_position[1],
               'inx': grid_position[2], 'iny': grid_position[3]}
    r = requests.post(url, json=payload)

app = FastAPI()

@app.get("/init")
async def init():
    print('User initiated dronesim...')

    init_dc_hosts()

    for dc_host in dc_hosts:
        if dc_host['status'] == 'Available':
            new_grid_position = get_grid()
            
            init_drone(dc_host, new_grid_position)
            time.sleep(2)

    return {"message": "Simulation started."}

@app.get("/droneupdate/{dc_id}")
def update_drone_inactive(dc_id: str):
    for dc in dc_hosts:
        if (dc_id == dc['host_id']):
            dc['status'] = 'Unavailable'
            return dc['host']

@app.post("/inferenceupdate")
async def update_from_inference(body):

    for dc_host in dc_hosts:
        if  body['id'] == dc_host['host_id']:
            print(f"Received an update from drone controlled {dc_host['host']}")

            if dc_host['status'] == 'Available':
                new_grid_position = get_grid()    
                move_drone(dc_host, new_grid_position)

            break

    return
