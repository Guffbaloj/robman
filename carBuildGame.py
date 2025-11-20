import pygame
from game import Game
from entity import Background, Entity, Dragable, Rob
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
        self.fonts = {"none": pygame.font.SysFont("arial", TEXT_SIZE),
                      "rob": pygame.font.SysFont("arial", TEXT_SIZE)}
        carpartImages = {  "back1":loadImage("carparts/back1.png",0.5),
                                "back2":loadImage("carparts/back2.png",0.5),
                                "back3":loadImage("carparts/back3.png",0.5),
                                "chassi1":loadImage("carparts/chassi.png",0.5),
                                "engine1":loadImage("carparts/engine1.png",0.5),
                                "engine2":loadImage("carparts/engine2.png",0.5),
                                "engine3":loadImage("carparts/engine3.png",0.5),
                                "front1":loadImage("carparts/front1.png",0.5),
                                "front2":loadImage("carparts/front2.png",0.5),
                                "front3":loadImage("carparts/front3.png",0.5),
                                "wheel1":loadImage("carparts/wheel1.png",0.5),} 
        RSM = 0.7
        robImages = { "worry1": loadImage("robImages/worry1.png", RSM),
                     "worry2": loadImage("robImages/worry2.png", RSM),
                     "neutral": loadImage("robImages/neutral.png", RSM),
                     "excited": loadImage("robImages/excited.png", RSM),
                     "angry1": loadImage("robImages/angry1.png", RSM),
                     "angry2": loadImage("robImages/angry2.png", RSM),
                     "side": loadImage("robright.png", RSM),}
        
        profiles = { "rob aah":loadImage("profiles/rob_aah.png"),
                     "rob angry1":loadImage("profiles/rob_angry1.png"),
                     "rob angry2":loadImage("profiles/rob_angry2.png"),
                     "rob dark":loadImage("profiles/rob_dark.png"),
                     "rob yay":loadImage("profiles/rob_yay.png"),
                     "rob neutral":loadImage("profiles/rob_neutral.png"),
                     "rob huh1":loadImage("profiles/rob_huh1.png"),
                     "rob huh2":loadImage("profiles/rob_huh2.png"),
                     "rob huh3":loadImage("profiles/rob_huh3.png"),
                     "rob worry1":loadImage("profiles/rob_worry1.png"),
                     "rob worry2":loadImage("profiles/rob_worry1.png"),
                     "none": loadImage("profiles/none.png")}
        
        self.images = {"base":loadImage("gurkman.png"),
                       "carpart": carpartImages,
                       "rob": robImages,
                       "profiles": profiles,
                       "background1": loadImage("carFactory.png"),
                       "background2": loadImage("bg1.png"),
                       }
        
        

        #ENTITIES
        self.carparts = {}
        self.snaprects = {}
        self.snaprectsList = [] #första är motorn, sista två är hjulen Följer snaprects ordning
        self.rob = Rob(self, (0,400),(100,100))
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
            carpart = Dragable(self, (xPos,yPos),hitboxSize, "carpart",self.snaprects[partType])
            try:
                img = self.images["carpart"][key]
            except:
                break
            carpart.setImage(key)
            self.carparts[partType].append(carpart)
            self.entities.append(carpart)
            self.rl3.append(carpart)
    
    def makeSnaprects(self, carCenter):
        self.snaprects = {"engine":[makeRect(carCenter, scaledPos(100, 100))],
                          "back":[makeRect(carCenter + scaledPos(-100, 0), scaledPos(100, 100))],
                         "front":[makeRect(carCenter + scaledPos(100, 0), scaledPos(100, 100))],
                         "wheel":[makeRect(carCenter + scaledPos(120, 80), scaledPos(50, 50)),
                                  makeRect(carCenter + scaledPos(-100, 80), scaledPos(50, 50))]}
        for carpart in self.snaprects:
            for snaprect in self.snaprects[carpart]:
                self.snaprectsList.append(snaprect)
    #===========================================
    #                SPELETS SCENER
    #===========================================
    def robArives(self, firstLoop):
        if firstLoop:
            self.rob.setPos(ROB_SIDE_ENTRANCE)
            self.rob.setImage("side")
            self.firstLoop = False
        
        done = self.rob.glideToPos(CENTER_POS, 2)   
        if done:
            self.firstLoop = True
            self.currentEvent = "rob talk"
        
    def robTalk(self, firstloop):
        if firstloop:
            self.activeTextIndex = 0
            self.rob.setPos(CENTER_POS)
            self.rob.setImage("neutral")
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
            self.rob.setImage("side")
        
        done = self.rob.glideToPos(ROB_CORNER, 2)

        if done:
            self.firstLoop = True
            self.currentEvent = "car game"
    
    def carGame(self, firstLoop):
        if firstLoop:
            self.rob.setPos(ROB_CORNER)
            self.rob.setImage("neutral")
            CAR_CENTER = CENTER_POS  + scaledPos(-10, +50)
            self.builtCar = [None, None, None, None, None]
            self.carparts = {"engine":[],"back":[],"front":[],"wheel":[]}
            self.makeSnaprects(CAR_CENTER)
            
            self.spawnCarparts((100,100),"engine",(75,75))
            self.spawnCarparts((100,100),"back",(100,100))
            self.spawnCarparts((100,100),"front",(100,100))
            self.spawnCarparts((100,100),"wheel",(50,50))
            self.spawnCarparts((100,100),"wheel",(50,50))
            self.firstLoop = False
        
        
        
