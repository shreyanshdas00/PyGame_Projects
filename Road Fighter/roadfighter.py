#%%
import pygame
import random
width=590
height=690
pygame.init()
win=pygame.display.set_mode((width,height))
pygame.display.set_caption("Road Fighter")
icon=pygame.image.load("icon.png")
pygame.display.set_icon(icon)
accelerate = pygame.USEREVENT
genpothole = pygame.USEREVENT+1
pygame.time.set_timer(accelerate, 3000)
pygame.time.set_timer(genpothole, 900)
grass=pygame.image.load('grass.png').convert_alpha()
track=pygame.image.load('track1.png').convert_alpha()
audience=pygame.image.load('audience.png').convert_alpha()
tree=pygame.image.load('tree.png').convert_alpha()
car=pygame.image.load('car.png').convert_alpha()
carsound=pygame.mixer.Sound('sound/car.wav')
blast=pygame.mixer.Sound('sound/blast.wav')
startbeep=pygame.mixer.Sound('sound/1startbeep.wav')
lastbeep=pygame.mixer.Sound('sound/laststartbeep.wav')
brake=pygame.mixer.Sound('sound/brake.wav')
def menu():
    f=2
    win.blit(grass,(0,0))
    win.blit(audience,(width/2,0))
    win.blit(track,(width/2-track.get_width(),0))
    win.blit(tree,(0,0))
    mfont=pygame.font.SysFont("candara",60)
    text1=mfont.render("ROAD",1,(255,0,0),True)
    win.blit(text1,((width-track.get_width()-text1.get_width())/2,200))
    mfont=pygame.font.SysFont("candara",60)
    text2=mfont.render("FIGHTER",1,(255,0,0),True)
    win.blit(text2,((width-track.get_width()-text2.get_width())/2,220+text1.get_height()))
    win.blit(car,((width-track.get_width()-car.get_width())/2,450))
    mfont=pygame.font.SysFont("candara",25)
    text3=mfont.render("PRESS UP ARROW KEY TO PLAY",1,(255,0,0),True)
    win.blit(text3,((width-track.get_width()-text3.get_width())/2,600))
    pygame.display.update()
    while f==2:
        keys=pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            f=0
            startbeep.play()
            pygame.time.delay(1000)
            startbeep.play()
            pygame.time.delay(1000)
            startbeep.play()
            pygame.time.delay(1000)
            lastbeep.play()
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                f=1
                pygame.quit()
                break
    return f
        

def main():
    pygame.time.delay(1000)
    pothole=pygame.image.load('pothole.png').convert_alpha()
    sign=pygame.image.load('sign.png').convert_alpha()
    blast1=pygame.image.load('blast1.png').convert_alpha()
    blast2=pygame.image.load('blast2.png').convert_alpha()
    holepos=[[-pothole.get_width(),0]]
    clock=pygame.time.Clock()
    groundcontrol=0
    carpos=(width-track.get_width()-car.get_width())/2
    f=0
    acc=0
    while True:
        clock.tick(100)
        for i in range(len(holepos)):
            if(holepos[i][1]>=height-car.get_height()-60 and holepos[i][1]<=height-80 and ((carpos>=holepos[i][0]+10 and carpos<=holepos[i][0]+pothole.get_width()-8)or(carpos+car.get_width()>=holepos[i][0]+10 and carpos+car.get_width()<=holepos[i][0]+pothole.get_width()-8)or(carpos>=holepos[i][0] and carpos+car.get_width()<=holepos[i][0]+pothole.get_width()))):
                carsound.set_volume(0)
                blast.play()
                win.blit(blast1,(carpos,height-car.get_height()-70))
                pygame.display.update()
                pygame.time.delay(600)
                win.blit(blast2,(carpos-28,height-car.get_height()-63))
                pygame.display.update()
                pygame.time.delay(2000)
                f=2
                break
        if f==0:
            win.blit(grass,(0,groundcontrol))
            win.blit(grass,(0,groundcontrol-grass.get_height()))
            win.blit(audience,(width/2,groundcontrol))
            win.blit(audience,(width/2,groundcontrol-audience.get_height()))
            win.blit(track,(width/2-track.get_width(),groundcontrol))
            win.blit(track,(width/2-track.get_width(),groundcontrol-track.get_height()))
            win.blit(tree,(0,groundcontrol))
            win.blit(tree,(0,groundcontrol-tree.get_height()))
            for i in range(len(holepos)):
                win.blit(pothole,(holepos[i][0],holepos[i][1]))
                win.blit(sign,(holepos[i][0]+(pothole.get_width()-sign.get_width())/2,holepos[i][1]+pothole.get_height()/2-sign.get_height()))
                holepos[i][1]+=3*acc
            win.blit(car,(carpos,height-car.get_height()-70))
            if groundcontrol>=track.get_height():
                groundcontrol=0
            else:
                groundcontrol+=3*acc
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    f=1
                    break
                if event.type == accelerate and acc<3:
                    acc*=1.15
                if event.type == genpothole and acc>1:
                    holeposx=random.randint(int(width/2-track.get_width()+7),int(width/2-7-pothole.get_width()))
                    holeposy=-groundcontrol-pothole.get_height()
                    holepos.append([holeposx,holeposy])
                    for item in holepos:
                        if item[1]>=height:
                            holepos.remove(item)
            keys=pygame.key.get_pressed()
            if keys[pygame.K_RIGHT]:
                if carpos>=width/2-38:
                    carpos=width/2-38
                else:
                    carpos+=1*acc
            if keys[pygame.K_LEFT]:
                if carpos<=width/2-track.get_width()+7:
                    carpos=width/2-track.get_width()+7
                else:
                    carpos-=1*acc
            if keys[pygame.K_DOWN]:
                carsound.set_volume(0)
                brake.play()
                acc=max(0,acc-0.15)
                if(acc>1):
                    carsound.set_volume(100)
            if keys[pygame.K_UP]:
                if acc<1:
                    carsound.play()
                    carsound.set_volume(100)
                    acc=1
            pygame.display.update()
        if f==1:
            pygame.quit()
            break
        if f==2:
            f=0
            break
    return f
if __name__=="__main__":
    while True:
        if(menu()==0):
            if(main()==0):
                pass
            else:
                break
        else:
            break
            