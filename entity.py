import pygame
import math
from utils import *
pygame.init()
class PhysicsObjects:
    def __init__(self, pos, size):
        self.pos = pygame.math.Vector2(pos)
        self.size = pygame.math.Vector2(size) * GAME_SCALE
        self.rect = pygame.rect.Rect(pos[0], pos[1], size[0], size[1])

    def move(self, movement, platforms):
        collisionTypes = {"up": False, "down": False, "left": False, "right": False}
        self.pos.x += movement[0]
        self.rect.x = int(self.pos.x)
        collisionList = getCollisions(self.rect, platforms)
        for block in collisionList:
            if movement[0] > 0:
                self.rect.right = block.left
                collisionTypes["right"] = True
            if movement[0] < 0:
                self.rect.left = block.right
                collisionTypes["left"] = True
            self.pos.x = self.rect.x

        self.pos.y += movement[1]
        self.rect.y = int(self.pos.y)
        collisionList = getCollisions(self.rect, platforms)
        for block in collisionList:
            if movement[1] > 0:
                self.rect.bottom = block.top
                collisionTypes["down"] = True
            if movement[0] < 0:
                self.rect.top = block.bottom
                collisionTypes["left"] = True
            self.pos.y = self.rect.y
        
        return collisionTypes
    def draw(self, display, offset): #Debug och sånt
        offsetPos = self.pos - offset
        offsetRect = pygame.rect.Rect(offsetPos.x, offsetPos.y, self.size.x, self.size.y)
        pygame.draw.rect(display,(33,233,211), offsetRect)

class Entity:
    def __init__(self, game, pos, size, eType):
        self.game = game
        self.pos = pygame.math.Vector2(pos)
        self.velocity = pygame.math.Vector2(0, 0)
        self.size = pygame.math.Vector2(size) * GAME_SCALE
        self.rect = pygame.rect.Rect(pos[0], pos[1], size[0], size[1])
        self.object = PhysicsObjects(pos, size)
        self.images = game.images
        self.imageKey = None
        self.flip = False
        self.type = eType
        self.wasPressed = False
        self.targetPos = None
    
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
        if math.dist(self.targetPos,self.pos) < 2:
            self.setPos(self.targetPos)
            self.targetPos = None
            self.velocity = pygame.math.Vector2(0, 0)
            done = True
        return done 
    def getImageRect(self):
        rect = self.images[self.imageKey].get_rect()
        rect.topleft = self.pos
        return rect
    def setImage(self, newKey):
        self.imageKey = newKey

    def setPos(self, newPos):
        self.pos = pygame.math.Vector2(newPos)
        self.object.pos = pygame.math.Vector2(newPos)
    def setCenter(self, newCenter):
        newPos = newCenter - self.size/2
        self.setPos(newPos)
    
    def move(self, movement, platforms):
        self.object.move(movement, platforms)
        self.setPos(self.object.pos)
        self.rect.topleft = self.object.pos

    def render(self, display = pygame.display.set_mode()):
        if self.imageKey:
            img = flip(self.images[self.imageKey], self.flip)
            imgWidth, imgHeight = img.get_size()
            display.blit(img, self.pos) # + (imgWidth / 2, imgHeight / 2))
        self.object.draw(display, [0, 0])
        self.draw(display, [0, 0])
    def onPress(self, mousePos):
        print("pah")
    def onHover(self, mousePos):
        pass
    def update(self):
        self.wasPressed = False
        self.move(self.velocity, [])
        
        mousePos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mousePos):
            self.onHover(mousePos)
            if self.game.main.justPressed == "mouse1":
                self.wasPressed = True
                self.onPress(mousePos)
    def draw(self, display, offset): #Debug och sånt
        offsetPos = self.pos - offset
        offsetRect = pygame.rect.Rect(offsetPos.x, offsetPos.y, self.size.x, self.size.y)
        pygame.draw.rect(display,(133,23,21), offsetRect)    

class Dragable(Entity):
    def __init__(self, game, pos, size, eType, snapRects):
        super().__init__(game, pos, size, eType)
        self.relativeMousePos = None    
        self.snapRects = snapRects
    
    def snapToCenter(self):
        collisions = getCollisions(self.rect, self.snapRects)
        if len(collisions) > 0:
            self.setCenter(collisions[0].center)
    def onPress(self, mousePos):
        self.getRelativeMousePos(mousePos)
    
    def getRelativeMousePos(self, mousePos):
        dX = self.pos.x - mousePos[0]
        dY = self.pos.y - mousePos[1]
        self.relativeMousePos = pygame.math.Vector2(dX, dY)

class Rob(Entity):
    def __init__(self, game, pos, size):
        super().__init__(game, pos, size, "rob")
