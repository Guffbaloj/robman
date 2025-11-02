import pygame
from utils import *
from dialog import robCarIntro
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
        
        
        self.draging = None
        self.rob = Rob((0,400),(100,100),self.main.images,self)
        self.gameState = "intro" #intro, game, end
        self.introState = "start"
        self.lastTalkIndex = None
    def spawnCarparts(self, pos, partType,hitboxSize):
        for i in range(1,100):
            key = partType + str(i)
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
    
    def manageDraging(self):
        self.draging = None
        for carpartType in self.carparts:
            for carpart in self.carparts[carpartType]:
                if carpart.isDraged:
                    self.draging = carpart
        if self.draging:
            self.draging.render(self.window)
    def updateAll(self):
        self.thing.update()
        self.rob.update()
        for carpartType in self.carparts:
            self.updateEntList(self.carparts[carpartType])
    def renderAll(self):
        #Snaprects och debug
        for carpartType in self.carparts:
            for snaprects in self.snaprects[carpartType]:
                pygame.draw.rect(self.window,(20,220,100),snaprects)
        
        #Faktiska spelet
        self.thing.render(self.window, True)
        for carpartType in self.carparts:
            self.renderEntList(self.carparts[carpartType],self.window)
        self.rob.render(self.window)
        if self.draging:
            self.draging.render(self.window)
    
    def runIntro(self):         
        if self.introState == "start":
            self.rob.setPos(ROB_SIDE_ENTRANCE)
            self.introState = "rob glide in"
        
        elif self.introState == "rob glide in": 
            self.rob.glideToPos(CENTER_POS,3)   
            if self.rob.targetPos == self.rob.pos:
                self.introState = "rob talk"
                self.rob.talkIndex = 0
                self.lastTalkIndex = None
        
        elif self.introState == "rob talk":
            if self.main.justPressed == "space":
                self.rob.talkIndex += 1
            if len(robCarIntro) > self.rob.talkIndex:
                if not self.rob.talkIndex == self.lastTalkIndex:
                    print(robCarIntro[self.rob.talkIndex])
                    self.lastTalkIndex = self.rob.talkIndex
                
            else:
                self.introState = "rob glide away"
        elif self.introState == "rob glide away":
            self.rob.glideToPos(ROB_CORNER,3)   
            if self.rob.targetPos == self.rob.pos:
                self.introState = "start game"
                self.rob.talkIndex = 0
                self.lastTalkIndex = None
        elif self.introState == "start game":
            self.spawnCarparts((100,100),"engine",(75,75))
            self.spawnCarparts((100,100),"back",(100,100))
            self.spawnCarparts((100,100),"front",(100,100))
            self.spawnCarparts((100,100),"wheel",(50,50))
            self.spawnCarparts((100,100),"wheel",(50,50))
            self.gameState = "game"

    def run(self):
        self.window.fill((255,255,255))
        if self.gameState == "intro":
            self.runIntro()
        elif self.gameState == "game":
            self.manageDraging()
        
        self.updateAll()
        self.renderAll()
        pygame.draw.rect(self.window,(100,100,100),self.snaprect1)
            
            
        pygame.display.update()