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
        
        buttonfont = pygame.font.SysFont("arial", 40)
        
        button1 = Button(self, START_BUTTON_POS, (80, 50), "Start", self.startButtonPress)
        button1.font = buttonfont
        button2 = Button(self, START_BUTTON_POS + scaledPos(0, 60), (120, 50), "Options", self.optionsButtonPress)
        button2.font = buttonfont
        button3 = Button(self, START_BUTTON_POS + scaledPos(0, 120), (65, 50), "Quit", self.quitButtonPress)
        button3.font = buttonfont
        
        self.entities.append(button1)
        self.entities.append(button2)
        self.entities.append(button3)
        
        #SETUP
        self.rl0.append(self.background)
        self.rlUI.append(button1)
        self.rlUI.append(button2)
        self.rlUI.append(button3)
    def optionsButtonPress(self):
        ...
    def quitButtonPress(self):
        pygame.quit()  
    def startButtonPress(self):
        self.main.loadNewScene("car game")
    
    def menu(self, firstLoop):
        if firstLoop:
            firstLoop = False
        