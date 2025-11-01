import pygame
from utils import *
from random import randrange
from entity import *

class Game:
    def __init__(self, main, display = pygame.display.set_mode((2,2))):
        self.main = main
        self.window = display
        self.snaprect1 = pygame.rect.Rect(250,250,40,40)
        self.thing = Dragable((200,200), (20,20), self.main.images, [self.snaprect1], self)
        self.carparts = {"engine":[],"back":[],"front":[],"wheel":[]}
        
        carCenterX, carCenterY = CENTER_POS
        self.snaprects = {"engine":[pygame.rect.Rect(carCenterX,carCenterY,100,100)],
                          "back":[pygame.rect.Rect(carCenterX-75,carCenterY,100,100)],
                         "front":[pygame.rect.Rect(carCenterX+75,carCenterY,100,100)],
                         "wheel":[pygame.rect.Rect(carCenterX-80,carCenterY+90,100,100),pygame.rect.Rect(carCenterX+75,carCenterY+90,100,100)]}
        
        self.spawnCarparts((100,100),"engine",(75,75))
        self.spawnCarparts((100,100),"back",(100,100))
        self.spawnCarparts((100,100),"front",(100,100))
        self.spawnCarparts((100,100),"wheel",(50,50))
        self.spawnCarparts((100,100),"wheel",(50,50))
        self.draging = None
    def spawnCarparts(self, pos, partType,hitboxSize):
        for i in range(1,100):
            key = partType + str(i)
            print(key)
            xPos = randrange(-50,50)+pos[0]
            yPos = randrange(-50, 50) + pos[1]
            carpart = Dragable((xPos,yPos),hitboxSize,self.main.images,self.snaprects[partType],self)
            try:
                img = self.main.images[key]
            except:
                break
            carpart.image = key
            self.carparts[partType].append(carpart)
    def updateEntList(self,list):
        for item in list:
            item.update()
    def renderEntList(self, list, display):
        for item in list:
            if not item == self.draging:
                item.render(display)
    def run(self):
        self.window.fill((255,255,255))
        self.thing.update()
        self.draging = None

        for carpartType in self.carparts:
            for carpart in self.carparts[carpartType]:
                if carpart.isDraged:
                    self.draging = carpart
                
        for carpartType in self.carparts:
            self.updateEntList(self.carparts[carpartType])
        pygame.draw.rect(self.window,(100,100,100),self.snaprect1)
        self.thing.render(self.window, True)
        for carpartType in self.carparts:
            for snaprects in self.snaprects[carpartType]:
                pygame.draw.rect(self.window,(20,220,100),snaprects)
        for carpartType in self.carparts:
            self.renderEntList(self.carparts[carpartType],self.window)
        if self.draging:
            self.draging.render(self.window)
        
        

        pygame.display.update()