import pygame
from textbox import Textbox
pygame.init()
HEIGHT = 640
WIDTH = 820

class Main:
    def __init__(self):
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        self.images = {}
        self.fonts = {"areal":pygame.font.SysFont("Areal",20)}
        self.textbox = Textbox((0,0),"0oooogofgodgfdfgsdfg",3,self.fonts["areal"])
    
    def run(self):
        while True:
            self.window.fill((255,255,255))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            self.textbox.sayText()
            self.textbox.update()
            self.textbox.drawText(self.window)
            pygame.display.update()

if __name__ == "__main__":
    Main().run()