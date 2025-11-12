import pygame
from game import Game
from utils import loadImage

class MainMenu(Game):
    def __init__(self, main, display):
        super().__init__(main, display)
        self.firstLoop = True
        self.currentEvent = "menu"
        self.events = {"menu":self.menu}
        self.images = {"background": loadImage("meny.png",1.5)}
        self.background = "background"
    
    def menu(self, firstLoop):
        if firstLoop:
            firstLoop = False