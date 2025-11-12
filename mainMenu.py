import pygame
from game import Game
from utils import *
from entity import Button
START_BUTTON_POS = CENTER_POS + (20 * X_POINT, 20 * Y_POINT)
class MainMenu(Game):
    def __init__(self, main, display):
        super().__init__(main, display)
        self.firstLoop = True
        self.currentEvent = "menu"
        self.events = {"menu":self.menu}
        self.images = {"background": loadImage("meny.png",0.75)}
        self.background = "background"
        startButtonImages = {"passive":loadImage("startPassive.png"), "active":loadImage("startActive.png")}
        self.optionsButton = ...
        self.startButton = Button(START_BUTTON_POS, startButtonImages, self)
        self.quitButton = ...
        self.entities.append(self.startButton)

    
    def menu(self, firstLoop):
        if firstLoop:
            firstLoop = False
        
        if self.startButton.wasPressed:
            print("wow")
            self.main.loadNewScene("car game")
        