import pygame
from game import Game
from utils import *
from entity import Background, Button
START_BUTTON_POS = CENTER_POS + scaledPos(110, 55)
class MainMenu(Game):
    def __init__(self, main, display):
        super().__init__(main, display)
        self.firstLoop = True
        self.currentEvent = "menu"
        self.events = { "menu":self.menu}
        startButton = { "passive":loadImage("startPassive.png"),
                        "active":loadImage("startActive.png")}
        self.images = { "background": loadImage("meny.png",0.75),
                        "start":startButton}
        self.background = Background(self.images["background"])
        startButton = Button(self, START_BUTTON_POS, (20, 40), "Start", self.startButtonPress)
        startButton.font = pygame.font.SysFont("arial", 20)
        self.entities.append(startButton)
        #SETUP
        self.rl0.append(self.background)
        self.rlUI.append(startButton)
        
    def startButtonPress(self):
        self.main.loadNewScene("car game")
    
    def menu(self, firstLoop):
        if firstLoop:
            firstLoop = False
        