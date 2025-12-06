from game import *

class FleeingGame(Game):
    def __init__(self, main, display):
        super().__init__(main, display)

        robImages = {"side":loadImage("robImages/side1.png", 0.3)}
        rogerImages = {}
        obstructions = {loadImage("junk/j1.png")}
        self.images = {"rob":robImages,
                       "roger": rogerImages,
                       "obst":obstructions}
        self.firstLoop = True
        self.events = {"start": self.startChase}
        self.currentEvent = "start"
        self.rob = Entity(self, CENTER_POS, (20, 20), "rob")
        self.rob.setImage("side")
        self.rl2.append(self.rob)
        self.entities.append(self.rob)
    def controllEntity(self, entity):
        key = pygame.key.get_pressed()

        if key[pygame.K_0]:
            print("ooo")
    
    def startChase(self, firstLoop):
        if firstLoop:
            self.firstLoop = False
        self.controllEntity("bah")