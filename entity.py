import pygame
from utils import loadImage
class Entity:
    def __init__(self, centerPos,images):
        self.pos = pygame.math.Vector2(centerPos)
        self.images = images
        self.image = "base"
        self.timer = 0

    def setPos(self,newX,newY):
        self.pos.x = newX
        self.pos.y = newY
    
    def getImageRect(self):
        rect = self.images[self.image].get_rect()
        rect.center = self.pos
        return rect
    
    def update(self):
        
    
    def render(self, display=pygame.display.set_mode((2,2))):
        image = self.images[self.image]
        width, height = image.get_size()
        display.blit(image,self.pos - (width/2, height/2))

class Rob(Entity):
    def __init__(self, centerPos,images):
        super().__init__(centerPos,images)
        self.image = "rob"
    
