import pygame
from game import Game
from entity import Dragable, Rob
from utils import *
from random import randrange
from dialog import robCarDialog

class CarBuildGame(Game):
    def __init__(self, main, display):
        super().__init__(main, display)        
        self.firstLoop = True
        self.currentEvent = "car game"
        self.events = {"start": self.robArives,
                        "rob talk": self.robTalk,
                        "rob glide away": self.robAway,
                        "car game": self.carGame}
        #BILDER OCH FONTER
        self.fonts = {"rob":pygame.font.SysFont("arial", TEXT_SIZE)}
        self.images = {"base":loadImage("gurkman.png"),
                       "rob":loadImage("rob1.png"),
                       "back1":loadImage("carparts/back1.png",0.5),
                       "chassi1":loadImage("carparts/chassi.png",0.5),
                       "engine1":loadImage("carparts/engine1.png",0.5),
                       "engine2":loadImage("carparts/engine2.png",0.5),
                       "engine3":loadImage("carparts/engine3.png",0.5),
                       "front1":loadImage("carparts/front1.png",0.5),
                       "front2":loadImage("carparts/front2.png",0.5),
                       "wheel1":loadImage("carparts/wheel1.png",0.5)}

        #ENTITIES
        self.carparts = {}
        self.snaprects = {}
        self.rob = Rob((0,400),(100,100),self.images,self)
        self.entities.append(self.rob)

        self.builtCar = {}
        
    def spawnCarparts(self, pos, partType,hitboxSize):
        
        
        
        for i in range(1,100):
            key = partType + str(i)
            xPos = randrange(-50,50)+pos[0]
            yPos = randrange(-50, 50) + pos[1]
            carpart = Dragable((xPos,yPos),hitboxSize,self.images,self.snaprects[partType],self)
            try:
                img = self.images[key]
            except:
                break
            carpart.image = key
            self.carparts[partType].append(carpart)
            self.entities.append(carpart)
    
    #===========================================
    #                SPELETS SCENER
    #===========================================
    def robArives(self, firstLoop):
        if firstLoop:
            self.rob.setPos(ROB_SIDE_ENTRANCE)

            self.firstLoop = False
        
        self.rob.glideToPos(CENTER_POS,3)   
        if self.rob.targetPos == self.rob.pos:
            self.firstLoop = True
            self.currentEvent = "rob talk"
        
    def robTalk(self, firstloop):
        if firstloop:
            self.activeTextIndex = 0
            self.previousTextIndex = None
            self.firstLoop = False
        
        self.handleDialog(robCarDialog) #slutar med att self.activeTextIndex sätts till "Done"
            
        if self.activeTextIndex == "Done":
            self.firstLoop = True
            self.currentEvent = "rob glide away"
        
    def robAway(self, firstLoop):
        if firstLoop:
            self.firstLoop = False
        
        self.rob.glideToPos(ROB_CORNER,3)
        if self.rob.targetPos == self.rob.pos:
            self.firstLoop = True
            self.currentEvent = "car game"
    def manageDraging(self):
        self.draging = None
        for entity in self.entities:
            if isinstance(entity, Dragable):
                if entity.isDraged:
                    self.draging = entity
                    
    def carGame(self, firstLoop):
        if firstLoop:
            carCenterX, carCenterY = CENTER_POS
            self.builtCar = [None, None, None, None, None]
            self.carparts = {"engine":[],"back":[],"front":[],"wheel":[]}
            self.snaprects ={"engine":[pygame.rect.Rect(carCenterX,carCenterY,100,100)],
                          "back":[pygame.rect.Rect(carCenterX-75,carCenterY,100,100)],
                         "front":[pygame.rect.Rect(carCenterX+75,carCenterY,100,100)],
                         "wheel":[pygame.rect.Rect(carCenterX-80,carCenterY+90,100,100),
                                  pygame.rect.Rect(carCenterX+75,carCenterY+90,100,100)]}
            self.spawnCarparts((100,100),"engine",(75,75))
            self.spawnCarparts((100,100),"back",(100,100))
            self.spawnCarparts((100,100),"front",(100,100))
            self.spawnCarparts((100,100),"wheel",(50,50))
            self.spawnCarparts((100,100),"wheel",(50,50))
            self.firstLoop = False
        currentSnaprect = 0
        for carparts in self.carparts:
            for snaprectList in self.snaprects[carparts]:
                for snaprect in snaprectList:
                    for carpart in self.carparts[carparts]:
                        if snaprect.collidepoint(carpart.getPos):
                            self.builtCar[currentSnaprect] = carpart
                    currentSnaprect += 1
        print(self.builtCar, currentSnaprect)


        print(self.builtCar)
