import socket
import threading

class server:

    def __init__(self):
        self.PORT = 5050
        self.SERVER = socket.gethostbyname(socket.gethostname())
        self.ADDR = (self.SERVER, self.PORT)

        self.HEADER = 128
        self.FORMAT = "utf-8"
        self.DISCONNECT_MESSAGE = "!DISCONNECT"

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.ADDR)
        self.serverup = True

        self.clients = []
    
    def add_client(self, client):
        self.clients.append(client)

    def respond(self, conn, msg):
        for client in self.clients:
            if msg == self.DISCONNECT_MESSAGE:
                message = msg.encode(self.FORMAT)
                msg_length = len(message)
                send_length = str(msg_length).encode(self.FORMAT)
                send_length += b" " * (self.HEADER - len(send_length))
                client[0].send(send_length)
                client[0].send(message)

            elif client[0] != conn:
                message = msg.encode(self.FORMAT)
                msg_length = len(message)
                send_length = str(msg_length).encode(self.FORMAT)
                send_length += b" " * (self.HEADER - len(send_length))
                client[0].send(send_length)
                client[0].send(message)

    def handle_client(self, conn, addr):
        print(f"[NEW CONNECTION] {addr} connected.")

        connected = True
        while connected:
            msg_length = conn.recv(self.HEADER).decode(self.FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode(self.FORMAT)
                if msg == self.DISCONNECT_MESSAGE:
                    connected = False
                    self.clients.remove((conn, addr))
                print(f"[{addr}] {msg}")
                self.respond(conn, f"[{str(addr[0])}] {msg}")

        conn.close()

    def start(self):
        self.server.listen()
        print(f"[LISTENING] server is listening on: {self.SERVER}:{self.PORT}")

        while self.serverup:
            conn, addr = self.server.accept()
            self.add_client((conn, addr))
            thread = threading.Thread(target=self.handle_client, args=(conn, addr))
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

    print("[STARTING] server is starting...")
    
def main():
    ser = server()
    ser.start()

if __name__ == "__main__":
    main()