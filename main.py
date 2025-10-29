import pygame
from game import Game
from entity import Entity, Rob
from utils import *
WIDTH = 820
HEIGHT = 640
CENTER_POS = pygame.math.Vector2(WIDTH/2,HEIGHT/2)
class Main:
    def __init__(self):
        self.window = pygame.display.set_mode((WIDTH,HEIGHT))
        self.images = {"base":loadImage("gurkman.png"),
                       "rob":loadImage("rob1.png")}
        self.rob = Rob(CENTER_POS,(30,30),self.images,self)
        self.game = Game(self,self.window)
        self.inputs = {"mouseDown":False}
    def run(self):
        while True:
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    ...
                if event.type == pygame.KEYUP:
                    ...
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.inputs["mouseDown"] = True
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.inputs["mouseDown"] = False
            self.game.run()
            

if __name__ == "__main__":
    Main().run()