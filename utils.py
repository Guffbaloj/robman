import pygame

BASE_PATH = "images/"

def loadImage(path):
    image = pygame.image.load(BASE_PATH+path)
    image.convert_alpha()
    return image