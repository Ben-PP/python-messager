import socket
import threading
from time import sleep

class client:

    def __init__(self):
        self.HEADER = 128
        self.PORT = 5050
        self.FORMAT = "utf-8"
        self.DISCONNECT_MESSAGE = "!DISCONNECT"
        self.SERVER = "172.16.160.16"
        self.USER = socket.gethostname()
        self.login()
        self.ADDR = (self.SERVER, self.PORT)

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(self.ADDR)
        self.connected = True
        print("[Connected]")
        self.send(f"[SERVER]: User {self.USER} joinded to conversation!")
    
    def login(self):

        srv = input("Server address(Default:172.16.160.16): ")
        if srv != "":
            self.SERVER = srv
        
        while True:
            try:
                prt = input("Port(Default:5050): ")
                if prt != "":
                    self.PORT = int(prt)
                break
            except:
                print(f"Give a number. <{prt}> is not a valid number")
        uname = input("Give username(Default: your IP): ")
        if uname != "":
            self.USER = uname

    def send(self, msg):
        message = msg.encode(self.FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(self.FORMAT)
        send_length += b" " * (self.HEADER - len(send_length))
        self.client.send(send_length)
        self.client.send(message)

    def listen(self):
        while self.connected:
            msg_length = self.client.recv(self.HEADER).decode(self.FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = self.client.recv(msg_length).decode(self.FORMAT)
                print(f"{msg}")

    
    def start(self):
        thread = threading.Thread(target=self.listen)
        thread.start()
        while self.connected:
            message = input()
            if message == "exit":
                self.send(f"[{self.USER}]: {self.DISCONNECT_MESSAGE}")
                self.connected = False
                sleep(1)
            else:
                self.send(f"[{self.USER}]: {message}")

        print("[Disconnected]")

def main():
    cli = client()
    cli.start()
    
if __name__ == "__main__":
    main()