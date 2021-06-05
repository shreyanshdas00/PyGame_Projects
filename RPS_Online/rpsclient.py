#%%
import pygame
from rpsnetwork import Network
from rpsgame import Game

width=500
height=500
pygame.init()
win=pygame.display.set_mode((width,height))
pygame.display.set_caption("Game client")
logo=pygame.image.load("rps.png")
pygame.display.set_icon(logo)


class Button:
    def __init__(self,text,x,y,color):
        self.text=text
        self.x=x
        self.y=y
        self.color=color
        self.width=136
        self.height=100
        
    def draw(self,win):
        pygame.draw.rect(win,self.color,(self.x,self.y,self.width,self.height))
        bfont=pygame.font.SysFont("candara",26)
        title=bfont.render(self.text,1,(255,255,255),True)
        win.blit(title,(self.x+self.width/2-title.get_width()/2,self.y+self.height/2-title.get_height()/2))
        
    def click(self,pos):
        x1=pos[0]
        y1=pos[1]
        if self.x<=x1<=self.x+self.width and self.y<=y1<=self.y+self.height:
            return True
        else:
            return False
            

def redrawwindow(win,game,p):
    win.fill((100,240,200))
    if not(game.connected()):
        mfont=pygame.font.SysFont("candara",45)
        text=mfont.render("Waiting for player...",1,(0,0,0),True)
        win.blit(text,(width/2-text.get_width()/2,height/2-text.get_height()/2))
    else:
        mfont=pygame.font.SysFont("candara",45)
        text=mfont.render("Your Move",1,(0,0,0),True)
        win.blit(text,(width/4-text.get_width()/2,100))
        text=mfont.render("Opponents",1,(0,0,0),True)
        win.blit(text,((3*width/4)-text.get_width()/2,100))
        move1=game.get_player_move(0)
        move2=game.get_player_move(1)
        if game.bothWent():
            text1=mfont.render(move1,1,(0,0,0),True)
            text2=mfont.render(move2,1,(0,0,0),True)
        else:
            if game.p1Went and p==0:
                text1=mfont.render(move1,1,(0,0,0),True)
            elif game.p1Went:
                text1=mfont.render("Locked in",1,(0,0,0),True)
            else:
                text1=mfont.render("Waiting...",1,(0,0,0),True)
            if game.p2Went and p==1:
                text2=mfont.render(move2,1,(0,0,0),True)
            elif game.p2Went:
                text2=mfont.render("Locked in",1,(0,0,0),True)
            else:
                text2=mfont.render("Waiting...",1,(0,0,0),True)
        if p==1:
            win.blit(text2,(width/4-text.get_width()/2,200))
            win.blit(text1,((3*width/4)-text.get_width()/2,200))
        else:
            win.blit(text1,(width/4-text.get_width()/2,200))
            win.blit(text2,((3*width/4)-text.get_width()/2,200))
        for btn in btns:
            btn.draw(win)
                
    pygame.display.update()
    
btns=[Button("ROCK",23,377,(0,0,0)),Button("PAPER",182,377,(0,0,0)),Button("SCISSORS",341,377,(0,0,0))]

def main():
    run=True
    clock=pygame.time.Clock()
    n=Network()
    player=int(n.getP())
    print("You are player ",player+1)
    flag=0
    while run:
        clock.tick(60)
        try:
            game=n.send("get")
        except:
            run=False
            print(f"Exiting game...Player {(player+1)%2+1} left")
            break
        if game.bothWent():
            redrawwindow(win,game,player)
            pygame.time.delay(500)
            try:
                game=n.send("reset")
            except:
                run=False
                print("Couldn't reset game...Lost connection")
                break
            mfont=pygame.font.SysFont("candara",70)
            if (game.winner()==1 and player==1) or (game.winner()==0 and player==0):
                fillc=(0,200,0)
                text=mfont.render("You Won!!",1,(255,255,255),True)
            elif game.winner()==-1:
                fillc=(0,0,200)
                text=mfont.render("Tie Game!",1,(255,255,255),True)
            else:
                fillc=(200,0,0)
                text=mfont.render("You Lost...",1,(255,255,255),True)
            win.fill(fillc)
            win.blit(text,(width/2-text.get_width()/2,height/2-text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(3000)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                flag=1
                run=False
                break
            if event.type==pygame.MOUSEBUTTONDOWN:
                pos=pygame.mouse.get_pos()
                for btn in btns:
                    if btn.click(pos) and game.connected():
                        if player==0:
                            if not game.p1Went:
                                n.send(btn.text)
                        else:
                            if not game.p2Went:
                                n.send(btn.text)
                                
        if run==True:
            redrawwindow(win,game,player)
    if flag==1:
        pygame.quit()
        return 0
    return 1
    
def menu():
    run=True
    flag=0
    clock=pygame.time.Clock()
    while run:
        clock.tick(60)
        win.fill((100,240,200))
        mfont=pygame.font.SysFont("candara",45)
        text=mfont.render("Press any key to play!",1,(0,0,0),True)
        win.blit(text,(width/2-text.get_width()/2,height/2-text.get_height()/2))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                flag=1
                run=False
                break
            if event.type==pygame.MOUSEBUTTONDOWN or event.type==pygame.KEYDOWN:
                run=False
                break
    if flag==1:
        pygame.quit()
        return 0
    return main() 
    
if __name__=="__main__":
    while menu():
        pass
    
