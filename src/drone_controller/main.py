import asyncio
import os

HOST = ''
PORT = int(os.environ['PORT'])

UAV_HOST = os.environ['UAV_HOST']
UAV_PORT = os.environ['UAV_PORT']

async def control_drone(position_data) -> None:
     pass
 
async def handle_incoming(self, reader, writer):
        data = await reader.read()
        payload = eval(data.decode())
        addr = writer.get_extra_info('peername')

        print(f'Received {payload} from {addr!r}')

        await control_drone(payload)

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
