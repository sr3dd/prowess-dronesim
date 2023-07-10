import asyncio
import os
import sys
import time

from models import Action, Grid

HOST = ''
PORT = int(os.environ['UAV_PORT'])

INFERENCE_SERVER_HOST = os.environ['INFERENCE_HOST']
INFERENCE_SERVER_PORT = os.environ['INFERENCE_PORT']

TRANSMIT_DELAY = float(os.environ['TRANSMIT_DELAY'])
INNER_MOTION_DELAY = float(os.environ['INNER_MOTION_DELAY'])
OUTER_MOTION_DELAY = float(os.environ['OUTER_MOTION_DELAY'])
TRANSMIT_DRAIN = float(os.environ['TRANSMIT_DRAIN'])
INNER_MOTION_DRAIN = float(os.environ['INNER_MOTION_DRAIN'])
OUTER_MOTION_DRAIN = float(os.environ['OUTER_MOTION_DRAIN'])


class UAV:
    def __init__(self) -> None:
        self._battery: float = 100
        self._outer_grid_size: int | None = None
        self._inner_grid_size: int | None = None
        self._outer_pos: int | None = None
        self._inner_pos: int | None = None

    def compute_distance(self, old_pos: int, new_pos: int, grid: Grid = Grid.OUTER) -> int:
        #placeholder
        return 1

    def init_position(self, outer_grid: int, inner_grid: int, 
                        outer_pos: int, inner_pos: int = 0) -> None:
        
        if self._outer_grid_size is not None:
            print('Drone already in grid')
            return
        
        self._outer_grid_size = outer_grid
        self._inner_grid_size = inner_grid
        self.move_outer(outer_pos, inner_pos)

    def move_outer(self, out_pos: int, in_pos: int = 0) -> None:
        self.decrement_battery(Action.MOVE_OUTER, out_pos, in_pos)
        self._outer_pos = out_pos
        self._inner_pos = in_pos

    def move_inner(self, in_pos: int) -> None:
        self.decrement_battery(Action.MOVE_INNER, inner_pos = in_pos)
        self._inner_pos = in_pos

    def get_status(self) -> None:
        print(f'Battery: {self._battery}\tOuter Position: {self._outer_pos}\tInner Postion: {self._inner_pos}')

    async def transmit_payload(self) -> None:
        self.decrement_battery(Action.TRANSMIT)
        reader, writer = await asyncio.open_connection(
        INFERENCE_SERVER_HOST, INFERENCE_SERVER_PORT)

        # a payload of ~9 MB
        image = 'abc'*3*1024

        print(f'Transmitting image...')
        writer.write(image.encode())
        await writer.drain()

        data = await reader.read()
        print(f'Received: {data.decode()!r}')

        print('Closing the connection')
        writer.close()
        await writer.wait_closed()

    def decrement_battery(self, action_type: Action, 
                            out_pos: int = None, inner_pos: int = None) -> None:
        
        match action_type:
            case Action.TRANSMIT:
                print('Battery consumption due to payload transmission')
                self._battery -= TRANSMIT_DRAIN
                time.sleep(TRANSMIT_DELAY)

            case Action.MOVE_INNER:
                print('Battery consumption due to inner move')
                distance = self.compute_distance(self._inner_grid_size, 
                                                self._inner_pos if self._inner_pos else 0, 
                                                inner_pos)
                self._battery -= INNER_MOTION_DRAIN*distance
                time.sleep(INNER_MOTION_DELAY*distance)

            case Action.MOVE_OUTER:
                print('Battery consumption due to outer move')
                outer_distance = self.compute_distance(self._inner_grid_size, 
                                                self._outer_pos if self._outer_pos else 0, 
                                                inner_pos)
                self._battery -= OUTER_MOTION_DRAIN*outer_distance
                time.sleep(OUTER_MOTION_DELAY*outer_distance)

                inner_distance = self.compute_distance(self._inner_grid_size, 
                                                self._inner_pos if self._inner_pos else 0, 
                                                inner_pos)
                self._battery -= INNER_MOTION_DRAIN*inner_distance
                time.sleep(INNER_MOTION_DELAY*inner_distance)

        if self._battery <= 0:
            sys.exit('Battery died.')
            
    async def handle_incoming(self, reader, writer):
        data = await reader.read()
        payload = eval(data.decode())
        addr = writer.get_extra_info('peername')

        print(f'Received {payload} from {addr!r}')

        match payload['do']:
            case 'init':
                if {'outer_grid', 'inner_grid', 'outer_pos'} <= set(payload):
                    if 'inner_pos' in payload:
                        self.init_position(payload['outer_grid'],
                                            payload['inner_grid'],
                                            payload['outer_pos'],
                                            payload['inner_pos'])
                    else:
                        self.init_position(payload['outer_grid'],
                                            payload['inner_grid'],
                                            payload['outer_pos'])
                else:
                    print('Init payload missing mandatory keys')
            case 'omove':
                if 'outer_pos' in payload:
                    if 'inner_pos' in payload:
                        self.move_outer(payload['outer_pos'],
                                        payload['inner_pos'])
                    else:
                        self.init_position(payload['outer_pos'])
                else:
                    print('Outer Move payload missing mandatory keys')
            case 'imove':
                if 'pos' in payload:
                    self.move_inner(payload['pos'])
                else:
                    print('Inner Move payload missing mandatory keys')

        self.get_status()

        print('\tSending ack...')
        writer.write('Received'.encode())
        await writer.drain()

        print('Closing the connection')
        writer.close()
        await writer.wait_closed()

        print('Initiating image transmission')
        await self.transmit_payload()

    async def fly(self) -> None:
        server = await asyncio.start_server(
                            self.handle_incoming, 
                            HOST, PORT)

        addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
        print(f'Serving on {addrs}')

        async with server:
            await server.serve_forever()
      