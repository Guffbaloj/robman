import pygame
from carBuildGame import CarBuildGame
from mainMenu import MainMenu
from utils import *
#import cProfile as profile

pygame.init()
class Main:
    def __init__(self):
        self.window = pygame.display.set_mode((WIDTH,HEIGHT))
        self.images = {"base":loadImage("gurkman.png")}
        
        self.scenes = {"main menu":  MainMenu,
                       "car game": CarBuildGame}
        
        self.currentScene = None
        
        self.inputs = {"mouseDown":False,
                        "space":False}
        self.clock = pygame.time.Clock()
        self.justPressed = None
        self.loadNewScene("main menu")
    
    def loadNewScene(self, newScene):
        self.currentScene = self.scenes[newScene](self, self.window)
    
    def run(self):
        while True:
            self.justPressed = None
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.inputs ["space"] = True
                        self.justPressed = "space"
                if event.type == pygame.KEYUP:
                        self.inputs ["space"] = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.inputs["mouseDown"] = True
                        self.justPressed = "mouse1"
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.inputs["mouseDown"] = False
            self.currentScene.run()
            self.clock.tick(FPS)
            

if __name__ == "__main__":
    #profile.run("Main().run()")
    Main().run()