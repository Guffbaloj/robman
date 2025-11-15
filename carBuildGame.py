import pygame
from game import Game
from entity import Dragable, Rob, Background
from utils import *
from random import randrange
from dialog import robCarDialog

#alla possitioner rob glider till
ROB_SIDE_ENTRANCE = (0, HEIGHT/2)
ROB_CORNER = CENTER_POS + scaledPos(160, 110)

class CarBuildGame(Game):
    def __init__(self, main, display):
        super().__init__(main, display)        
        self.firstLoop = True
        self.currentEvent = "start"
        self.events = {"start": self.robArives,
                        "rob talk": self.robTalk,
                        "rob glide away": self.robAway,
                        "car game": self.carGame}
        #BILDER OCH FONTER
        self.fonts = {"base": pygame.font.SysFont("arial", TEXT_SIZE),
                      "rob": pygame.font.SysFont("arial", TEXT_SIZE)}
        self.images = {"base":loadImage("gurkman.png"),
                       "back1":loadImage("carparts/back1.png",0.5),
                       "back2":loadImage("carparts/back2.png",0.5),
                       "back3":loadImage("carparts/back3.png",0.5),
                       "chassi1":loadImage("carparts/chassi.png",0.5),
                       "engine1":loadImage("carparts/engine1.png",0.5),
                       "engine2":loadImage("carparts/engine2.png",0.5),
                       "engine3":loadImage("carparts/engine3.png",0.5),
                       "front1":loadImage("carparts/front1.png",0.5),
                       "front2":loadImage("carparts/front2.png",0.5),
                       "front3":loadImage("carparts/front3.png",0.5),
                       "wheel1":loadImage("carparts/wheel1.png",0.5),
                       "background1": loadImage("carFactory.png"),
                       "background2": loadImage("bg1.png")}
        

        #ENTITIES
        self.carparts = {}
        self.snaprects = {}
        self.rob = Rob((0,400),(100,100),self)
        self.entities.append(self.rob)

        self.builtCar = {}

        #SETUP
        self.background1 = Background(self.images["background1"])
        self.background2 = Background(self.images["background2"])
        self.rl0.append(self.background1)
        self.rl2.append(self.background2)
        self.rl4.append(self.rob)

    def spawnCarparts(self, pos, partType,hitboxSize):
        
        pos = scaledPos(pos[0], pos[1])
        hitboxSize = scaledPos(hitboxSize[0], hitboxSize[1])
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
            self.rl3.append(carpart)
    
    #===========================================
    #                SPELETS SCENER
    #===========================================
    def robArives(self, firstLoop):
        if firstLoop:
            self.rob.setPos(ROB_SIDE_ENTRANCE)
            self.rob.setImage("right")
            self.firstLoop = False
        
        done = self.rob.glideToPos(CENTER_POS, 2)   
        if done:
            self.firstLoop = True
            self.currentEvent = "rob talk"
        
    def robTalk(self, firstloop):
        if firstloop:
            self.activeTextIndex = 0
            self.rob.setPos(CENTER_POS)
            self.rob.setImage("front")
            self.previousTextIndex = None
            self.firstLoop = False
            self.generalTimer = 0
        if self.generalTimer < 1 * FPS:
            self.generalTimer += 1
        else:
            self.handleDialog(robCarDialog) #slutar med att self.activeTextIndex sätts till "Done"
            
        if self.activeTextIndex == "Done":
            self.firstLoop = True
            self.currentEvent = "rob glide away"
        
    def robAway(self, firstLoop):
        if firstLoop:
            self.firstLoop = False
            self.rob.setPos(CENTER_POS)
            self.rob.setImage("right")
        self.rob.glideToPos(ROB_CORNER, 2)
        
        if self.rob.targetPos == self.rob.pos:
            self.firstLoop = True
            self.currentEvent = "car game"
                    
    def carGame(self, firstLoop):
        if firstLoop:
            self.rob.setPos(ROB_CORNER)
            self.rob.setImage("front")
            CAR_CENTER = CENTER_POS  + scaledPos(-10, +50)
            self.builtCar = [None, None, None, None, None]
            self.carparts = {"engine":[],"back":[],"front":[],"wheel":[]}
            self.snaprects ={"engine":[makeRect(CAR_CENTER, scaledPos(100, 100))],
                          "back":[makeRect(CAR_CENTER + scaledPos(-100, 0), scaledPos(100, 100))],
                         "front":[makeRect(CAR_CENTER + scaledPos(100, 0), scaledPos(100, 100))],
                         "wheel":[makeRect(CAR_CENTER + scaledPos(120, 80), scaledPos(50, 50)),
                                  makeRect(CAR_CENTER + scaledPos(-100, 80), scaledPos(50, 50))]}
            
            self.spawnCarparts((100,100),"engine",(75,75))
            self.spawnCarparts((100,100),"back",(100,100))
            self.spawnCarparts((100,100),"front",(100,100))
            self.spawnCarparts((100,100),"wheel",(50,50))
            self.spawnCarparts((100,100),"wheel",(50,50))
            self.firstLoop = False
        currentSnaprect = 0
        """for carparts in self.carparts:
            for snaprectList in self.snaprects[carparts]:
                for snaprect in snaprectList:
                    for carpart in self.carparts[carparts]:
                        if snaprect.collidepoint(carpart.getPos):
                            self.builtCar[currentSnaprect] = carpart
                    currentSnaprect += 1
        print(self.builtCar, currentSnaprect)"""
