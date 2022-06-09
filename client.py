import socket
import threading
from time import sleep

from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

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
        self.has_sym_key = False

        self.private_key = self.gen_asym_keys(None)
        self.public_key = self.gen_asym_keys(self.private_key)

        self.send(self.public_key.export_key().decode())

        self.SYM_KEY = self.receive_sym_key()
        self.has_sym_key = True

        print("[Connected]")
        self.send(f"[SERVER]: User {self.USER} joinded to conversation!")

    def receive_sym_key(self):
        msg_length = self.client.recv(self.HEADER).decode(self.FORMAT)
        if msg_length:
            decrypt = PKCS1_OAEP.new(key=self.private_key)
            msg_length = int(msg_length)
            msg = self.client.recv(msg_length)
            decrypted_msg = decrypt.decrypt(msg)
            return decrypted_msg

    def gen_asym_keys(self, key):
        if key is None:
            return RSA.generate(2048)
        else:
            return key.public_key()
    
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

    def encrypt(self, msg):
        cipher = AES.new(self.SYM_KEY, AES.MODE_CBC)
        ciphered_msg = cipher.encrypt(pad(msg,AES.block_size))
        ciphered_msg = ciphered_msg+cipher.iv
        return ciphered_msg

    def send(self, msg):
        if self.has_sym_key:
            message = self.encrypt(msg.encode(self.FORMAT))
        else:
            message = msg.encode(self.FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(self.FORMAT)
        send_length += b" " * (self.HEADER - len(send_length))

        #TODO: 5. Encrypt using servers symmetric key
        self.client.send(send_length)
        self.client.send(message)

    def listen(self):
        while self.connected:
            msg_length = self.client.recv(self.HEADER).decode(self.FORMAT)
            #TODO: 4. Decrypt using servers symmetric key
            if msg_length:
                msg_length = int(msg_length)
                msg = self.client.recv(msg_length).decode(self.FORMAT)
                #TODO: 4. Decrypt using servers symmetric key
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