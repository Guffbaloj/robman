import pygame
from game import Game
from utils import *
from entity import Background, Entity
START_BUTTON_POS = CENTER_POS + scaledPos(110, 55)
class MainMenu(Game):
    def __init__(self, main, display):
        super().__init__(main, display)
        self.firstLoop = True
        self.currentEvent = "menu"
        self.events = { "menu":self.menu}
        self.images = { "background": loadImage("meny.png",0.75),
                        "start passive":loadImage("startPassive.png"),
                        "start active":loadImage("startActive.png")}
        self.background = Background(self.images["background"])
        self.startButton = Entity(self, START_BUTTON_POS, (50, 50), "start")
        self.startButton.setImage("start passive")
        self.entities.append(self.startButton)
        #SETUP
        self.rl0.append(self.background)
        self.rlUI.append(self.startButton)
        

    
    def menu(self, firstLoop):
        if firstLoop:
            firstLoop = False
        if self.startButton.wasPressed:
            self.main.loadNewScene("car game")
        