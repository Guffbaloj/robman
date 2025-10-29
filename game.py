import pygame
from utils import loadImage
from entity import *

class Game:
    def __init__(self, main, display = pygame.display.set_mode((2,2))):
        self.main = main
        self.window = display
        self.snaprect1 = pygame.rect.Rect(250,250,40,40)
        self.thing = Dragable((200,200), (20,20), self.main.images, self.snaprect1, self)
    
    def run(self):
        self.window.fill((255,255,255))
        self.thing.update()
        pygame.draw.rect(self.window,(100,100,100),self.snaprect1)
        self.thing.render(self.window, True)

        
        
        

        pygame.display.update()