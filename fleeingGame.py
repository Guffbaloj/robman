from game import *


class FleeingGame(Game):
    def __init__(self, main, display):
        super().__init__(main, display)

        robImages = {"side":loadImage("robImages/side1.png", 0.3)}
        rogerImages = {}
        obstructions = {"j1":loadImage("junk/j1.png"), 
                        "j2":loadImage("junk/j2.png"),
                        "j3":loadImage("junk/j3.png"),
                        "j4":loadImage("junk/j4.png"),
                        "j5":loadImage("junk/j5.png"),

                        "j6":loadImage("junk/j6.png", 0.5),
                        "j7":loadImage("junk/j7.png", 0.5),
                        "j8":loadImage("junk/j8.png", 0.5),
                        "j9":loadImage("junk/j9.png", 0.5),
                        "j10":loadImage("junk/j10.png", 0.5),
                        "j11":loadImage("junk/j11.png", 0.5),
                        "j12":loadImage("junk/j12.png", 0.5),
                        "j13":loadImage("junk/j13.png", 0.5),}
        self.images = {"rob":robImages,
                       "roger": rogerImages,
                       "obst":obstructions}
        self.firstLoop = True
        self.events = {"start": self.startChase}
        self.currentEvent = "start"
        self.rob = Entity(self, CENTER_POS, (20, 20), "rob")
        self.rob.setImage("side")
        self.rob.friction = 0 #förvirrande att noll innebär hundra procent friction, kanske borde heta "glide" eller något liknande i framtida projekt. Det får en verkligen att fundera på verklgheten och alla sådana grejer som variabelnamn kansek inte. 
        self.rl2.append(self.rob)
        self.entities.append(self.rob)

        self.obsticles = []
        self.fleeSpeed = 3
        self.obsTimer = 0
        self.obsSpawnTime = 10
    def controllEntity(self, entity):
        key = pygame.key.get_pressed()

        if key[pygame.K_w]:
            entity.move((0, -2))
        
        if key[pygame.K_s]:
            entity.move((0, 2))
    def updateObsticles(self):
        obsticles = self.obsticles.copy()
        for object in obsticles:
            object.move((-self.fleeSpeed, 0))
            if object.pos.x < 0 -object.size.x:
                self.rl2.remove(object)
                self.obsticles.remove(object)
                self.entities.remove(object)
    def spawnObsticles(self):
        self.obsTimer += 1
        if self.obsTimer > self.obsSpawnTime:
            obst = Entity(self, (WIDTH + 30, randrange(0, HEIGHT)), (20, 20), "obst")
            obst.setImage("j"+str(randrange(0, len(self.images["obst"])) + 1))
            
            self.entities.append(obst)
            self.obsticles.append(obst)
            self.RLHeightInsert(obst, self.rl2)
            self.obsTimer = 0
    def orderRob(self):
        self.rl2.remove(self.rob)
        self.RLHeightInsert(self.rob, self.rl2)

    def startChase(self, firstLoop):
        if firstLoop:
            self.firstLoop = False
        
        self.orderRob()
        self.controllEntity(self.rob)
        self.spawnObsticles()
        self.updateObsticles()