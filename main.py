import pygame
WIDTH = 820
HEIGHT = 640
class Main:
    def __init__(self):
        self.window = pygame.display.set_mode((WIDTH,HEIGHT))
    
    def run(self):
        while True:
            self.window.fill((255,255,255))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            
            pygame.display.update()

if __name__ == "__main__":
    Main().run()