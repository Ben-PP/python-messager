HEADER = 128
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

clients = []

def add_client(client):
    clients.append(client)


def respond(conn, msg):
    for client in clients:
        if client[0] != conn:
            message = msg.encode(FORMAT)
            msg_length = len(message)
            send_length = str(msg_length).encode(FORMAT)
            send_length += b" " * (HEADER - len(send_length))
            client[0].send(send_length)
            client[0].send(message)

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False
                clients.remove((conn, addr))
            print(f"[{addr}] {msg}")
            respond(conn, msg)

    conn.close()