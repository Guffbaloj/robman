import pygame
from utils import loadImage
class Entity:
    def __init__(self, centerPos,hitboxSize,images, game):
        self.game = game
        self.pos = pygame.math.Vector2(centerPos)
        self.images = images
        self.image = "base"
        self.timer = 0
        self.hitbox = pygame.rect.Rect(0,0,hitboxSize[0],hitboxSize[1])
        self.hitbox.center = centerPos

    def setPos(self,newPos):
        newX, newY = newPos
        self.pos.x = newX
        self.pos.y = newY
        self.hitbox.center = (newX, newY)
    
    def getImageRect(self):
        rect = self.images[self.image].get_rect()
        rect.center = self.pos
        return rect
    
    def update(self):
        ...
    
    def render(self, display, showHitbox = False):
        image = self.images[self.image]
        width, height = image.get_size()
        display.blit(image,self.pos - (width/2, height/2))
        if showHitbox:
            pygame.draw.rect(display,(130,130,130,20),self.hitbox)


class Dragable(Entity):
    def __init__(self, centerPos, hitboxSize, images, snaprect, game):
        super().__init__(centerPos, hitboxSize, images, game)
        self.snaprect = snaprect
    
    def snapToCenter(self):
        if self.getImageRect().colliderect(self.snaprect):
            self.setPos(self.snaprect.center)
    
    def update(self):
        super().update()
        mousePos = pygame.mouse.get_pos()
        isDraged = False
        mouseDown = self.game.main.inputs["mouseDown"]
        if mouseDown:
            if self.hitbox.collidepoint(mousePos):
                isDraged = True
                self.setPos(mousePos)
        
        
        if not isDraged:   
            self.snapToCenter()

class Rob(Entity):
    def __init__(self, centerPos, hitboxSize, images, game):
        super().__init__(centerPos, hitboxSize, images, game)
        self.image = "rob"
    
