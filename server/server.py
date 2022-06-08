import re
import socket
import threading

class server:

    def __init__(self):
        #TODO: 1. Generate asymmetric key
        #TODO: 1. Generate symmetric key
        self.PORT = 5050
        self.SERVER = socket.gethostbyname(socket.gethostname())
        self.ADDR = (self.SERVER, self.PORT)

        self.HEADER = 128
        self.FORMAT = "utf-8"
        self.DISCONNECT_MESSAGE = "!DISCONNECT"

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(self.ADDR)
        self.serverup = True

        self.clients = []
    
    def add_client(self, client):
        self.clients.append(client)

    def respond(self, conn, msg):

        uname = msg.split(" ")
        msg_section = uname[1]
        uname = uname[0][1:-2:1]

        
        if msg_section == self.DISCONNECT_MESSAGE:
            message = f"[SERVER]: User {uname} disconnected".encode(self.FORMAT)
            msg_length = len(message)
            send_length = str(msg_length).encode(self.FORMAT)
            send_length += b" " * (self.HEADER - len(send_length))
            for client in self.clients:
                #TODO: 7. Encrypt using servers symmetric key
                client[0].send(send_length)
                client[0].send(message)
        else:
            message = msg.encode(self.FORMAT)
            msg_length = len(message)
            send_length = str(msg_length).encode(self.FORMAT)
            send_length += b" " * (self.HEADER - len(send_length))
            for client in self.clients:
                if client[0] == conn:
                    continue
                #TODO: 7. Encrypt using servers symmetric key
                client[0].send(send_length)
                client[0].send(message)

    #TODO: 2. client_handler class needed?
    def handle_client(self, conn, addr):
        print(f"[NEW CONNECTION] {addr} connected.")
        #TODO: 3. Send public key to client.
        #TODO: 4. Receive symmetric key from client
        #TODO: 5. Send server symmetric key to client 
        connected = True
        while connected:
            msg_length = conn.recv(self.HEADER).decode(self.FORMAT)
            #TODO:  6. Decrypt received message with symmetric key
            if msg_length:
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode(self.FORMAT)
                #TODO: 6. Decrypt received message with symmetric key
                regex_msg = re.search(self.DISCONNECT_MESSAGE, msg)

                if regex_msg != None:
                    connected = False
                    self.clients.remove((conn, addr))
                    print(f"[{addr}] {msg}")
                    self.respond(conn, msg)
                    break

                print(f"[{addr}] {msg}")
                self.respond(conn, msg)

        conn.close()

    def start(self):
        self.sock.listen()
        print(f"[LISTENING] server is listening on: {self.SERVER}:{self.PORT}")

        while self.serverup:
            conn, addr = self.sock.accept()
            self.add_client((conn, addr))
            thread = threading.Thread(target=self.handle_client, args=(conn, addr))
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

    print("[STARTING] server is starting...")
    
def main():
    serv = server()
    serv.start()

if __name__ == "__main__":
    main()