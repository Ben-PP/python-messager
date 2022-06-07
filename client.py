import socket
import threading
from time import sleep

HEADER = 128
PORT = 5050
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "172.16.160.25"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)
connected = True
print("[Connected]")

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b" " * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)

def listen():
    while connected:
        msg_length = client.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = client.recv(msg_length).decode(FORMAT)
            print(f"{msg}")

thread = threading.Thread(target=listen)
thread.start()

while connected:
    message = input()
    if message == "exit":
        send(DISCONNECT_MESSAGE)
        connected = False
        sleep(1)
    else:
        send(message)

print("[Disconnected]")