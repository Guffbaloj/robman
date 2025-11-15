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
        
    def glideToPos(self, newPos, duration):
        done = False
        newTarget = pygame.math.Vector2(newPos)
       
        if self.targetPos != newTarget:
            self.targetPos = newTarget 
            dX = newPos[0] - self.pos.x
            dY = newPos[1] - self.pos.y
            
            xStep = dX/(duration*FPS)
            yStep = dY/(duration*FPS)
            self.velocity = pygame.math.Vector2(xStep,yStep)
        if self.targetPos == self.pos:
            done = True
        return done
            
        
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
                    self.velocity = None
    
    def render(self, display, showHitbox = False):
        image = self.images[self.image]
        width, height = image.get_size()
        display.blit(image,self.pos - (width/2, height/2))
        if showHitbox:
            pygame.draw.rect(display,(130,130,130,20),self.hitbox)

class Button(Entity):
    #En button måste ta in två bilder. Första är hover bilden, andra är 
    def __init__(self, centerPos, images, game):
        super().__init__(centerPos, (1, 1), images, game)
        self.image = "passive"
        self.hitbox = self.getImageRect()
        self.wasPressed = False
    
    def update(self):
        super().update()
        mousePos = pygame.mouse.get_pos()
        self.wasPressed = False
        if self.hitbox.collidepoint(mousePos):
            self.image = "active"
            if self.game.main.justPressed == "mouse1":
                self.wasPressed = True
        else:
            self.image = "passive"
        
class Background:
    def __init__(self, image):
        self.image = image
    def setBackground(self, newImage):
        self.image = newImage
    def render(self, display):
        display.blit(self.image, (0,0))


class Dragable(Entity):
    def __init__(self, centerPos, hitboxSize, images, snaprects, game):
        super().__init__(centerPos, hitboxSize, images, game)
        self.snaprects = snaprects
        self.hasSnaped = False
        self.relativeMousePos = None
    def snapToCenter(self):
        for snaprect in self.snaprects:
            if self.getHitbox().colliderect(snaprect):
                self.setPos(snaprect.center)
                break
    def getRelativeMousePos(self, mousePos):
        dX = self.pos.x - mousePos[0]
        dY = self.pos.y - mousePos[1]
        self.relativeMousePos = pygame.math.Vector2(dX, dY)

    def update(self):
        super().update()
        self.hasSnaped = False
        for snaprect in self.snaprects:
            if snaprect.center == self.pos:
                self.hasSnaped = True

class Rob(Entity):
    def __init__(self, centerPos, hitboxSize, game):
        super().__init__(centerPos, hitboxSize, None, game)
        self.image = "front neutral"
        self.images = {"front neutral":loadImage("robFront.png"),
                       "front worry":loadImage("robOrolig.png"),
                     "left neutral":loadImage("robLeft.png"),
                     "right neutral":loadImage("robRight.png"),}

    def setImage(self, direction, emotion = "neutral"):
        self.image = direction + " " + emotion
    def doSpecial(self, specialList):
        if "rob worry" in specialList:
            self.setImage("front","worry")
        elif "rob neutral"in specialList:
            self.setImage("front", "neutral")
    def update(self):
        super().update()
        
        if len(self.game.textEvent) > 0:
            self.doSpecial(self.game.textEvent)
