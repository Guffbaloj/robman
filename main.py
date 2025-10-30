import pygame
from game import Game
from entity import Entity, Rob
from utils import *

class Main:
    def __init__(self):
        self.window = pygame.display.set_mode((WIDTH,HEIGHT))
        self.images = {"base":loadImage("gurkman.png"),
                       "rob":loadImage("rob1.png"),
                       "back1":loadImage("carparts/back1.png",0.5),
                       "chassi1":loadImage("carparts/chassi.png",0.5),
                       "engine1":loadImage("carparts/engine1.png",0.5),
                       "engine2":loadImage("carparts/engine2.png",0.5),
                       "engine3":loadImage("carparts/engine3.png",0.5),
                       "front1":loadImage("carparts/front1.png",0.5),
                       "wheel1":loadImage("carparts/wheel1.png",0.5)}
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