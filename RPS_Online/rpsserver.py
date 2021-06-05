#%%
import socket
from _thread import *
import pickle
from rpsgame import Game

server="192.168.1.13"
port=5555

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

try:
    s.bind((server,port))
except socket.error as e:
    print(e)
    
s.listen(2)#2=max number of clients
print("Waiting for a connection, Server Started")

games={}
idCount=0

def threaded_client(conn,player,gameId):
    global idCount
    conn.send(str(player).encode("utf-8"))
    while True:
        try:
            data=conn.recv(4096).decode("utf-8")
            if gameId in games:
                game=games[gameId]
                
                if not data:
                    print("Disconnected: ", player+1)
                    break
                else:
                    if data=="reset":
                        game.resetWent()
                    elif data!="get":
                        game.play(player,data)
                    conn.sendall(pickle.dumps(game))
            else:
                break
        except:
            break
        
    print(f"Player {player+1} left")
    try:
        del games[gameId]
        print("Closing game: ",gameId)
    except:
        pass
    idCount-=1
    conn.close()

if __name__=="__main__":            
    while True:
        conn,addr=s.accept()
        print("Connected to: ",addr)
        idCount+=1
        p=0
        gameId=(idCount-1)//2
        if idCount%2==1:
            games[gameId]=Game(gameId)
            print("Creating a new game")
        else:
            games[gameId].ready=True
            p=1
        start_new_thread(threaded_client,(conn,p,gameId))
    
