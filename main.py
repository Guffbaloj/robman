import pygame
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
        self.rob = Rob(CENTER_POS,self.images)
    def run(self):
        while True:
            self.window.fill((255,255,255))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            self.rob.render(self.window)
            pygame.display.update()

if __name__ == "__main__":
    Main().run()