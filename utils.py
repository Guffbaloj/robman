import pygame

BASE_PATH = "images/"
WIDTH = 820
HEIGHT = 640
CENTER_POS = pygame.math.Vector2(WIDTH/2,HEIGHT/2)
FPS = 60

def loadImage(path, size = 1):
    image = pygame.image.load(BASE_PATH+path)
    image.convert_alpha()
    height, width = image.get_size()
    image = pygame.transform.scale(image,(height*size, width*size))
    return image

def pygameQuitEvent():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
