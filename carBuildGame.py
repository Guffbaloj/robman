import pygame
from game import Game
from entity import *
from utils import *
from random import randrange
from carGameDialog import *

#alla possitioner rob glider till
ROB_SIDE_ENTRANCE = (0, HEIGHT/2)
ROB_CORNER = CENTER_POS + scaledPos(160, 110)
ROB_THROW_POS = CENTER_POS + scaledPos(-50, - HEIGHT / 5)
BUTTON_POS = (WIDTH - 100 * GAME_SCALE, HEIGHT - 80 * GAME_SCALE)
CARPARTSS = ["engine", "back", "front", "wheel"]
class CarBuildGame(Game):
    def __init__(self, main, display):
        super().__init__(main, display)        
        self.firstLoop = True
        self.currentEvent = "car game"
        self.events = {"start": self.robArives,
                        "rob talk": self.robTalk,
                        "rob glide away": self.robAway,
                        "rob in again": self.robIn,
                        "car game": self.carGame,
                        "asking rob": self.askingRobForParts}
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
                     "side": loadImage("robImages/side1.png", RSM),
                     "dig1": loadImage("robImages/dig1.png", RSM),
                     "dig1": loadImage("robImages/dig1.png", RSM),
                     "dig2": loadImage("robImages/dig2.png", RSM)}
        junk ={"j1":loadImage("junk/j1.png"), 
               "j2":loadImage("junk/j2.png"),
               "j3":loadImage("junk/j3.png"),
               "j4":loadImage("junk/j4.png"),
               "j5":loadImage("junk/j5.png"),}
        profiles = { "rob aah":loadImage("profiles/rob_aah.png"),
                    "rob oh":loadImage("profiles/rob_oh.png"),
                    "rob annoyed1":loadImage("profiles/rob_annoyed1.png"),
                     "rob angry1":loadImage("profiles/rob_angry1.png"),
                     "rob angry2":loadImage("profiles/rob_angry2.png"),
                     "rob angry3":loadImage("profiles/rob_angry3.png"),
                     "rob dark":loadImage("profiles/rob_dark.png"),
                     "rob yay":loadImage("profiles/rob_yay.png"),
                     "rob neutral":loadImage("profiles/rob_neutral.png"),
                     "rob huh1":loadImage("profiles/rob_huh1.png"),
                     "rob huh2":loadImage("profiles/rob_huh2.png"),
                     "rob huh3":loadImage("profiles/rob_huh3.png"),
                     "rob nervouse":loadImage("profiles/rob_nervouse.png"),
                     "rob worry1":loadImage("profiles/rob_worry1.png"),
                     "rob worry2":loadImage("profiles/rob_worry1.png"),
                     "none": loadImage("profiles/none.png")}
        
        self.images = {"base":loadImage("gurkman.png"),
                       "carpart": carpartImages,
                       "rob": robImages,
                       "profiles": profiles,
                       "junk": junk,
                       "background1": loadImage("carFactory.png"),
                       "background2": loadImage("bg1.png"),
                       }
        
        

        #ENTITIES
        self.carparts = {}
        self.snaprects = {}
        self.snaprectsList = [] #första är motorn, sista två är hjulen Följer snaprects ordning
        self.rob = Rob(self, (0,400),(100,100))
        self.entities.append(self.rob)

        self.builtCar = {"engine": None, "back":None, "front":None, "wheel1":None, "wheel2":None}

        #SETUP
        self.background1 = Background(self.images["background1"])
        self.background2 = Background(self.images["background2"])
        self.rl0.append(self.background1)
        self.rl2.append(self.background2)
        self.rl4.append(self.rob)
        
        self.floorRect = makeRect(CENTER_POS + scaledPos(0, HEIGHT / 2), (WIDTH, 20 * GAME_SCALE))
        self.thrownItems = []
        self.thrownJunk = []
        self.spawningCarparts = False
        self.carpartSpawnTimer = 0
        self.carpartToThrow = 0
        self.carpartTalkIdx = 0
    
   
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
    
    def throwJunk(self, pos, strenght, objIndx):
        pos = scaledPos(pos[0], pos[1])
        object = Entity(self, pos, (2, 2), "junk")
        object.setVelocity(strenght)
        object.setAcceleration((0, BASE_GRAVITY / 2))
        object.setImage("j"+str(objIndx + 1))
        self.entities.append(object)
        self.rl1.append(object)
        self.thrownJunk.append(object)
    
    def spawnTrownCarpart(self, pos, strenght, partType, hitboxSize, imgidx):
        pos = scaledPos(pos[0], pos[1])
        hitboxSize = scaledPos(hitboxSize[0], hitboxSize[1])
        object = Entity(self, pos, hitboxSize, "carpart")
        object.velocity = pygame.Vector2(strenght)
        object.friction = 0.99
        object.setAcceleration((0, BASE_GRAVITY / 2))
        object.setCollidables([self.floorRect])
        object.setImage(partType + str(imgidx))
        object.scale = 0.4
        object.extra = partType
        self.thrownItems.append(object)
        self.entities.append(object)
        self.rl1.append(object)
    
    def carpartFromEnt(self, ent):
        snaprects = self.snaprects[ent.extra]
        print(self.snaprects[ent.extra])
        print(snaprects)
        carpart = Dragable(self, ent.pos, ent.size, "carpart", snaprects)
        carpart.setImage(ent.imageKey)
        carpart.friction = 0.99
        carpart.setVelocity((0, ent.velocity.y))
        carpart.setAcceleration(ent.acceleration)
        carpart.setAcceleration((0, BASE_GRAVITY))
        carpart.setCollidables([self.floorRect])
        return carpart

    def makeSnaprects(self, carCenter):
        self.snaprects = {"engine":[SnapRect(carCenter, scaledPos(100, 100))],
                          "back":[SnapRect(carCenter + scaledPos(-100, 0), scaledPos(100, 100))],
                         "front":[SnapRect(carCenter + scaledPos(100, 0), scaledPos(100, 100))],
                         "wheel":[SnapRect(carCenter + scaledPos(120, 80), scaledPos(50, 50)),
                                  SnapRect(carCenter + scaledPos(-100, 80), scaledPos(50, 50))]}
        for carpart in self.snaprects:
            for snaprect in self.snaprects[carpart]:
                self.snaprectsList.append(snaprect)
    
    def askForMoreCarparts(self):
        if not self.spawningCarparts and self.currentEvent == "car game":
            print("wooouuu")
            self.firstLoop = True
            self.currentEvent = "asking rob"
            
        else:
            print("vänta lite mannen!")
    
    def handleThrownItems(self):
        for item in self.thrownItems.copy():
            if item.velocity.y >= 0:
                carpart = self.carpartFromEnt(item)
                
                self.thrownItems.remove(item)
                self.rl1.remove(item)
                self.entities.remove(item)
                self.rl3.append(carpart)
                self.entities.append(carpart)
        
        for item in self.thrownJunk.copy():
            if item.pos.x > WIDTH or item.pos.y > HEIGHT:
                self.entities.remove(item)
                self.rl1.remove(item)
                self.thrownJunk.remove(item)
    
    def robTrowAnimation(self, timer): #Måste bli snyggare framöver
        if int(timer) % 2 == 0:
            self.rob.setImage("dig1")
        elif int(timer) % 2 == 1:
            self.rob.setImage("dig2")
    
    def throwCarparts(self, idx, partType, pos, size):
        key = partType + str(idx)
        xPos = randrange(-50,50)+pos[0]
        yPos = randrange(-50, 50) + pos[1]
        try:
            img = self.images["carpart"][key]
        except:
            return True
        self.spawnTrownCarpart(pos, (randrange(-4, 4), -26), partType, size, idx)
        return False
    #===========================================
    #                SPELETS SCENER
    #===========================================
    def askingRobForParts(self, fistLoop):
        if fistLoop:
            self.activeTextIndex = 0
            self.firstLoop = False
            self.showTalkButtons = False
            self.rob.setImage("neutral")
            if self.carpartTalkIdx >= len(carpartDialog):
                self.carpartTalkIdx = len(carpartDialog) - 1
        
        done = self.handleDialog(carpartDialog[self.carpartTalkIdx])
        if done:
            self.spawningCarparts = True
            self.carpartSpawnTimer = 0
            self.generalTimer = 0
            self.carpartTalkIdx += 1
            self.currentEvent = "car game"
            
            
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
            done = self.handleDialog(robCarDialog) #slutar med att self.activeTextIndex sätts till "Done"
            
            if done:
                self.firstLoop = True
                self.currentEvent = "rob glide away"
        
    def robAway(self, firstLoop):
        if firstLoop:
            self.firstLoop = False
            self.rob.setPos(CENTER_POS)
            self.rob.setImage("side")
        
        done = self.rob.glideToPos(CENTER_POS + scaledPos(WIDTH, 0), 2)

        if done:
            self.firstLoop = True
            self.currentEvent = "rob in again"
    def robIn(self, firstLoop):
        if firstLoop:
            self.rob.scale = 0.4
            self.rl4.remove(self.rob)
            self.rl1.append(self.rob)
            self.rob.flip = True
            self.rob.setImage("side")
            self.rob.setPos(CENTER_POS + scaledPos(WIDTH, - HEIGHT / 5))
            self.firstLoop = False
        
        done = self.rob.glideToPos(ROB_THROW_POS, 3)
        
        if done:
            self.firstLoop = True
            self.currentEvent = "car game"

    def carGame(self, firstLoop):
        if firstLoop:
            if self.rob in self.rl4:
                self.rob.scale = 0.4
                self.rl4.remove(self.rob)
                self.rl1.append(self.rob)
                self.rob.flip = True

            self.rob.setPos(ROB_THROW_POS)
            CAR_CENTER = CENTER_POS  + scaledPos(-10, +50)
            self.builtCar = [None, None, None, None, None]
            self.carparts = {"engine":[],"back":[],"front":[],"wheel":[]}
            self.makeSnaprects(CAR_CENTER)
            
            button = Button(self, BUTTON_POS, (240, 40), "BE OM FLER DELAR", self.askForMoreCarparts)
            button.font = self.fonts["rob"]
            self.rlDB.append(button)
            self.entities.append(button)
            self.firstLoop = False
            self.generalTimer = 0
            self.spawningCarparts = False
            self.carpartSpawnTimer = 0
            self.carpartTalkIdx = 0
            self.askForMoreCarparts()
            self.showTalkButtons = False

        if self.spawningCarparts:  
            self.carpartSpawnTimer += 1
            if self.carpartToThrow > 3:
                self.carpartToThrow = 3
            print(self.carpartSpawnTimer)
            tajm = 32
            if int(self.carpartSpawnTimer) % tajm == 0:
                carpartType = CARPARTSS[self.carpartToThrow]
                done = self.throwCarparts(int(self.carpartSpawnTimer) // tajm, carpartType, ROB_THROW_POS + (randrange(-50, -40), -10), (80, 80))
                if done:
                    self.spawningCarparts = False
                    self.carpartSpawnTimer = 0
                    self.carpartToThrow += 1
        
        self.handleThrownItems()
        self.robTrowAnimation(self.generalTimer)

        
        self.throwJunk(self.rob.pos + (randrange(-50, -40), 0), (randrange(10, 15), randrange(-8, -5)),randrange(0, 5))
        

        self.generalTimer = self.generalTimer + 0.10
        
        if self.generalTimer > 20:
            self.showTalkButtons = True
        if self.generalTimer > 10000:
            self.generalTimer = 0
        
        
    

 #self.spawnCarparts((100,100),"engine",(75,75))
#self.spawnCarparts((100,100),"back",(100,100))
#self.spawnCarparts((100,100),"front",(100,100))
#self.spawnCarparts((100,100),"wheel",(50,50))
#self.spawnCarparts((100,100),"wheel",(50,50))       
        
        
