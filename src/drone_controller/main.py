import os
import socket

HOST = os.environ['UAV_HOST']  # The server's hostname or IP address
PORT = os.environ['UAV_PORT']  # The port used by the server

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = (HOST, PORT)

try:

    # Send data
    print('sending "%s"' % message)
    sent = sock.sendto(message.encode(), (server_address))

    # Receive response
    print('waiting to receive')
    data, server = sock.recvfrom(4096)
    print('received "%s"' % data)

finally:
    print('closing socket')
    sock.close()
