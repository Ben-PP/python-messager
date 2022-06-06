import socket
import threading

import handle_client

PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

HEADER = 128
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def start():
    server.listen()
    print(f"[LISTENING] server is listening on: {SERVER}:{PORT}")
    while True:
        conn, addr = server.accept()
        handle_client.add_client((conn, addr))
        thread = threading.Thread(target=handle_client.handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

print("[STARTING] server is starting...")
start()