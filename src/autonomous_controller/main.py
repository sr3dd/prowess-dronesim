import asyncio
import os
import time

class DroneInformation:
     pass

HOST = ''
PORT = int(os.environ['PORT'])

DRONE_CONTROLLER_HOST = os.environ['DRONE_CONTROLLER_HOST']
DRONE_CONTROLLER_PORT = os.environ['DRONE_CONTROLLER_PORT']

OUTER_GRID = int(os.environ['OUTER_GRID'])
INNER_GRID = int(os.environ['INNER_GRID'])

def init_drones() -> list[DroneInformation]:
     pass

async def notify_controller(position_data, drone_info_records: list[DroneInformation]) -> None:
     pass
 
async def handle_incoming(self, reader, writer, drones):
        data = await reader.read()
        payload = eval(data.decode())
        addr = writer.get_extra_info('peername')

        print(f'Received {payload} from {addr!r}')
        await notify_controller(payload, drones)

async def server() -> None:
    drones = init_drones()

    server = await asyncio.start_server(
                            lambda r, w: handle_incoming(r, w, drones), 
                            HOST, PORT)

    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    print(f'Serving on {addrs}')

    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(server())
