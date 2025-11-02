import pygame
import math
from utils import *
class Entity:
    def __init__(self, centerPos,hitboxSize,images, game):
        self.game = game
        self.pos = pygame.math.Vector2(centerPos)
        self.images = images
        self.image = "base"
        self.timer = 0
        self.hitbox = pygame.rect.Rect(0,0,hitboxSize[0],hitboxSize[1])
        self.hitbox.center = centerPos
        self.targetPos = None
        self.velocity = None
    def glideToPos(self, newPos, time):
        newTarget = pygame.math.Vector2(newPos)
       
        if self.targetPos != newTarget:
            self.targetPos = newTarget 
            dX = newPos[0] - self.pos.x
            dY = newPos[1] - self.pos.y
            
            xStep = dX/(time*FPS)
            yStep = dY/(time*FPS)
            self.velocity = pygame.math.Vector2(xStep,yStep)
            
        
    def setPos(self,newPos):
        newX, newY = newPos
        self.pos.x = newX
        self.pos.y = newY
        self.hitbox.center = (newX, newY)
    def getHitbox(self):
        rect = self.hitbox
        rect.center = self.pos
        return rect
    def getImageRect(self):
        rect = self.images[self.image].get_rect()
        rect.center = self.pos
        return rect
    
    def update(self):
        if self.velocity:
            self.pos += self.velocity
        
            if self.targetPos:
                if math.dist(self.targetPos,self.pos) < 2:
                    self.pos = self.targetPos
                    self.targetPos = None
    
    def render(self, display, showHitbox = False):
        image = self.images[self.image]
        width, height = image.get_size()
        display.blit(image,self.pos - (width/2, height/2))
        if showHitbox:
            pygame.draw.rect(display,(130,130,130,20),self.hitbox)


class Dragable(Entity):
    def __init__(self, centerPos, hitboxSize, images, snaprects, game):
        super().__init__(centerPos, hitboxSize, images, game)
        self.snaprects = snaprects
        self.isDraged = False
    def snapToCenter(self):
        for snaprect in self.snaprects:
            
            if self.getHitbox().colliderect(snaprect):
                self.setPos(snaprect.center)
                break
    
    def update(self):
        super().update()
        mousePos = pygame.mouse.get_pos()
        mouseDown = self.game.main.inputs["mouseDown"]
        if self.game.draging == None or self.game.draging == self:
            if mouseDown:
                if self.hitbox.collidepoint(mousePos):
                    self.isDraged = True
                    self.targetPos = None
                
                if self.isDraged:
                    self.setPos(mousePos)
            else:
                self.isDraged = False
            
            if not self.isDraged:   
                self.snapToCenter()

class Rob(Entity):
    def __init__(self, centerPos, hitboxSize, images, game):
        super().__init__(centerPos, hitboxSize, images, game)
        self.image = "rob"
        self.talkIndex = 0
    
