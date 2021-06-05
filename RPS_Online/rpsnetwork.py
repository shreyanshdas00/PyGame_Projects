#%%
import socket
import pickle

class Network:
    def __init__(self):
        self.client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server="192.168.1.13"
        self.port=5555
        self.addr=(self.server,self.port)
        self.p=self.connect()
        
    def getP(self):
        return self.p
        
    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(4096).decode("utf-8")
        except Exception as e:
            print(e)
        
    def send(self,data):
        try:
            self.client.send(data.encode("utf-8"))
            return pickle.loads(self.client.recv(4096))
        except socket.error as e:
            print(e)
             