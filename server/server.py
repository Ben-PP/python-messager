import socket
import threading

import handle_client

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

    def start(self):
        self.server.listen()
        print(f"[LISTENING] server is listening on: {self.SERVER}:{self.PORT}")

        while self.serverup:
            conn, addr = self.server.accept()
            handle_client.add_client((conn, addr))
            thread = threading.Thread(target=handle_client.handle_client, args=(conn, addr))
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

    print("[STARTING] server is starting...")
    
def main():
    ser = server()
    ser.start()

if __name__ == "__main__":
    main()