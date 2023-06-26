import asyncio
import os
import time

HOST = ''
PORT = int(os.environ['PORT'])

AUTO_CONTROLLER_HOST = os.environ['AUTO_CONTROLLER_HOST']
AUTO_CONTROLLER_PORT = os.environ['AUTO_CONTROLLER_PORT']

INFERENCE_DELAY = float(os.environ['INFERENCE_DELAY'])

async def notify_controller(position_data) -> None:
     pass
 
async def handle_incoming(self, reader, writer):
        data = await reader.read()
        payload = eval(data.decode())
        addr = writer.get_extra_info('peername')

        print(f'Received {payload} from {addr!r}')
        time.sleep(INFERENCE_DELAY)
        await notify_controller(payload)

async def server() -> None:
    server = await asyncio.start_server(
                            handle_incoming, 
                            HOST, PORT)

    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    print(f'Serving on {addrs}')

    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(server())
