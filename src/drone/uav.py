import os
import sys
import time

import requests

from .models import Action

DC_HOST = os.environ['DC_HOST']
DC_PORT = os.environ['DC_PORT']
INFERENCE_HOST = os.environ['INFERENCE_HOST']
INFERENCE_PORT = os.environ['INFERENCE_PORT']

TRANSMIT_DELAY = float(os.environ['TRANSMIT_DELAY'])
INNER_MOTION_DELAY = float(os.environ['INNER_MOTION_DELAY'])
OUTER_MOTION_DELAY = float(os.environ['OUTER_MOTION_DELAY'])
TRANSMIT_DRAIN = float(os.environ['TRANSMIT_DRAIN'])
INNER_MOTION_DRAIN = float(os.environ['INNER_MOTION_DRAIN'])
OUTER_MOTION_DRAIN = float(os.environ['OUTER_MOTION_DRAIN'])

def compute_distance(old_pos, new_pos):
    #placeholder
    return 1.0

class UAV:
    def __init__(self) -> None:
        self._dc_id = None
        self._battery: float = 100
        self._outerx: int = 0
        self._outery: int = 0
        self._innerx: int = 0
        self._innery: int = 0

    def init_position(self, grid_pos, dc_id):
        self._dc_id = dc_id
        self.decrement_battery(Action.MOVE_OUTER, (grid_pos[0], grid_pos[1]))
        self._outerx = grid_pos[0]
        self._outery = grid_pos[1]
        self._innerx = grid_pos[2]
        self._innery = grid_pos[3]

    def move(self, new_pos):

        if (self._outerx, self._outery) != (new_pos[0], new_pos[1]):
            self.decrement_battery(Action.MOVE_OUTER, (new_pos[0], new_pos[1]))
        else:
            self.decrement_battery(Action.MOVE_INNER, (new_pos[2], new_pos[3]))

        self._outerx = new_pos[0]
        self._outery = new_pos[1]
        self._innerx = new_pos[2]
        self._innery = new_pos[3]
        return
        
    def get_status(self):
        return f'Battery: {self._battery}\tOuter Position: ({self._outerx}, {self._outery})\tInner Postion: ({self._innerx}, {self._innery})'
        

    def transmit_payload(self) -> None:
        self.decrement_battery(Action.TRANSMIT)

        # a payload of ~9 MB
        image = 'abc'*3*1024

        url = f'http://{INFERENCE_HOST}:{INFERENCE_PORT}/infer'

        payload = {'dc_id': self._dc_id, 'outx': self._outerx, 'outy': self._outery,
                    'inx': self._innerx, 'iny': self._innery, 'image': image}

        r = requests.post(url, json=payload)

        return r
    
    def decrement_battery(self, action_type: Action, 
                            new_pos = None):
        
        match action_type:
            case Action.TRANSMIT:
                print('Battery consumption due to payload transmission')
                self._battery -= TRANSMIT_DRAIN
                time.sleep(TRANSMIT_DELAY)

            case Action.MOVE_INNER:
                print('Battery consumption due to inner move')
                distance = compute_distance((self._innerx, self._innery), new_pos)
                self._battery -= INNER_MOTION_DRAIN*distance
                time.sleep(INNER_MOTION_DELAY*distance)

            case Action.MOVE_OUTER:
                print('Battery consumption due to outer move')
                distance = compute_distance((self._outerx, self._outery), new_pos)
                self._battery -= OUTER_MOTION_DRAIN*distance
                time.sleep(OUTER_MOTION_DELAY*distance)

        if self._battery <= 0:
            url = f'http://{DC_HOST}:{DC_PORT}/kill'
            r = requests.get(url)
            print(r.response)
            sys.exit('Battery died.')
      