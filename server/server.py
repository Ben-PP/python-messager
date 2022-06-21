import os
import re
import socket
import threading

from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

class server:

    def __init__(self):
        self.SYM_KEY = self.gen_sym_key()

        self.PORT = 5060
        self.SERVER = socket.gethostbyname(socket.gethostname())
        self.ADDR = (self.SERVER, self.PORT)

        self.HEADER = 128
        self.FORMAT = "utf-8"
        self.DISCONNECT_MESSAGE = "!DISCONNECT"

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(self.ADDR)
        self.serverup = True

        self.clients = []
    
    def gen_sym_key(self):
        AES_key_length = 32
        sym_key = os.urandom(AES_key_length)
        return sym_key
    
    def add_client(self, client):
        self.clients.append(client)
    
    def remove_client(self, client):
        self.clients.remove(client)

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
                try:
                    client[0].send(send_length)
                    client[0].send(message)
                except BrokenPipeError:
                    print("[ERROR] BrokenPipeError")
        else:
            message = msg.encode(self.FORMAT)
            msg_length = len(message)
            send_length = str(msg_length).encode(self.FORMAT)
            send_length += b" " * (self.HEADER - len(send_length))
            for client in self.clients:
                try:
                    if client[0] == conn:
                        continue
                    client[0].send(send_length)
                    client[0].send(message)
                except BrokenPipeError:
                    print("[ERROR] BrokenPipeError")

    def receive_pub_key(self, conn):
        msg_length = conn.recv(self.HEADER).decode(self.FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(self.FORMAT)
            client_pub_key = RSA.import_key(msg)
        return client_pub_key
    
    def send_sym_key(self, conn, pub_key):
        cipher = PKCS1_OAEP.new(key=pub_key)
        cipher_msg = cipher.encrypt(self.SYM_KEY)
        msg_length = len(cipher_msg)
        send_length = str(msg_length).encode(self.FORMAT)
        send_length += b" " * (self.HEADER - len(send_length))
        conn.send(send_length)
        conn.send(cipher_msg)
        
    def handle_client(self, conn, addr):
        print(f"[NEW CONNECTION] {addr} connected.")
        client_pub_key = self.receive_pub_key(conn)
        self.send_sym_key(conn, client_pub_key)
        connected = True
        while connected:
            msg_length = conn.recv(self.HEADER).decode(self.FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = conn.recv(msg_length)
                iv = msg[-16:]
                cipher = AES.new(self.SYM_KEY, AES.MODE_CBC, iv)
                msg = unpad(cipher.decrypt(msg[0:-16:]), AES.block_size)
                msg = msg.decode(self.FORMAT)

                regex_msg = re.search(self.DISCONNECT_MESSAGE, msg)
                if regex_msg != None:
                    connected = False
                    self.clients.remove((conn, addr))
                    print(f"[{addr}] {msg}")
                    break

                print(f"[{addr}] {msg}")
                self.respond(conn, msg)
            else:
                self.remove_client((conn, addr))
                break
        conn.close()

    def start(self):
        self.sock.listen()
        print(f"[LISTENING] server is listening on: {self.SERVER}:{self.PORT}")

        while self.serverup:
            conn, addr = self.sock.accept()
            self.add_client((conn, addr))
            thread = threading.Thread(target=self.handle_client, args=(conn, addr))
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

    print("[STARTING] server is starting...")
    
def main():
    serv = server()
    serv.start()

if __name__ == "__main__":
    main()