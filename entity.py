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
            if movement[1] < 0:
                self.rect.top = block.bottom
                collisionTypes["left"] = True
            self.pos.y = self.rect.y
        
        return collisionTypes
    def draw(self, display, offset): #Debug och sånt
        offsetPos = self.pos - offset
        offsetRect = pygame.rect.Rect(offsetPos.x, offsetPos.y, self.size.x, self.size.y)
        pygame.draw.rect(display,(255,233,211), offsetRect)

class Entity:
    def __init__(self, game, pos, size, eType):
        self.game = game
        self.pos = pygame.math.Vector2(pos)
        self.velocity = pygame.math.Vector2(0, 0)
        self.acceleration = pygame.math.Vector2(0, 0)
        self.friction = 1
        self.size = pygame.math.Vector2(size) * GAME_SCALE
        self.object = PhysicsObjects(pos, size)
        self.images = game.images[eType]
        self.imageKey = None
        self.flip = False
        self.type = eType
        self.wasPressed = False
        self.targetPos = None
        self.scale = 1
        self.platforms = []
        self.extra = None

    def setCollidables(self, platformList):
        self.platforms = platformList

    def resize(self, newScale):
        newSize = (int(self.size[0] * newScale), int(self.size[1] * newScale))
        self.object = PhysicsObjects(self.pos, newSize)
    
    def getRect(self):
        rect = pygame.rect.Rect(0, 0, self.size.x * self.scale, self.size.y * self.scale)
        rect.center = self.pos
        return rect
    
    def getImageRect(self):
        rect = self.images[self.imageKey].get_rect()
        rect.center = self.pos
        return rect
    
    def glideToPos(self, newPos, duration):
        done = False
        newTarget = pygame.math.Vector2(newPos)
        if self.targetPos != newTarget:
            self.targetPos = newTarget
            dX = newPos[0] - (self.pos.x + self.size.x/2)
            dY = newPos[1] - (self.pos.y + self.size.y/2)
            
            xStep = dX/(duration*FPS)
            yStep = dY/(duration*FPS)
            self.velocity = pygame.math.Vector2(xStep,yStep)
        if math.dist(self.targetPos,self.pos) < 100:
            self.setPos(self.targetPos)
            self.targetPos = None
            self.velocity = pygame.math.Vector2(0, 0)
            done = True
        return done 
    
    def setImage(self, newKey):
        self.imageKey = newKey

    def setPos(self, newPos):
        self.pos = pygame.math.Vector2(newPos) - self.size/2    
        self.object.pos = pygame.math.Vector2(newPos) - self.size/2
    def setVelocity(self, newVel):
        self.velocity = pygame.math.Vector2(newVel)
        
    def setAcceleration(self, newAcc):
        self.acceleration = pygame.math.Vector2(newAcc)
    
    def move(self, movement, platforms):
        collided = self.object.move(movement, platforms)
        self.setPos(self.object.pos + self.size/2)     
        if collided["down"] or collided["up"]:
            self.velocity.y = 0
        if collided["left"] or collided["right"]:
            self.velocity.x = 0
    
    def onPress(self, mousePos):
        pass
    def onHover(self, mousePos):
        pass

    def checkIfPressed(self):
        mousePos = pygame.mouse.get_pos()
        if self.getRect().collidepoint(mousePos):
            self.onHover(mousePos)
            if self.game.main.justPressed == "mouse1":
                self.wasPressed = True
                self.onPress(mousePos)
    def handleTextEvents(self, events):
        ...
    def update(self):
        self.wasPressed = False
        self.velocity += self.acceleration
        self.velocity *= self.friction
        self.move(self.velocity, self.platforms)
        self.checkIfPressed()
        if len(self.game.textEvent) > 0:
            self.handleTextEvents(self.game.textEvent)
       
    
    def draw(self, display): #Debug och sånt
        pygame.draw.rect(display,(133,23,21), self.getRect())    
    
    def render(self, display):
        if self.imageKey:
            #print("rendering", id(self.images[self.imageKey]))
            img = flip(self.images[self.imageKey], self.flip)
            img = scaleImage(img, self.scale)
            imgWidth, imgHeight = img.get_size()
            display.blit(img, self.pos - (imgWidth / 2, imgHeight / 2))
            #pygame.draw.rect(display, (20,255,20), self.getImageRect()) #Debug
        #self.object.draw(display, [0, 0]) #Debug
        #self.draw(display) #Debug

class SnapRect:
    def __init__(self, pos, size):
        self.pos = pygame.Vector2(pos)
        self.size = pygame.Vector2(size)
        self.rect = makeRect(pos, size)
        self.occupant = None
class Button:
    def __init__(self, game, pos, size, text, onPressFunction):
        self.pos = pygame.Vector2(pos)
        self.size = pygame.Vector2(size)
        self.text = text
        self.rect = makeRect(self.pos, self.size)
        self.onPressFunction = onPressFunction
        self.hovering = False
        self.game = game
        self.font = pygame.font.Font()
        self.color = (0, 0, 0)
        self.borderColor = (255, 255, 255)
        self.textColor = (255, 255, 255)
    def setFont(self, newFont):
        self.font = newFont
    
    def onHover(self):
        self.hovering = True
    
    def update(self):
        mousePos = pygame.mouse.get_pos()
        self.hovering = False
        if self.rect.collidepoint(mousePos):
            self.onHover()
            if self.game.main.justPressed == "mouse1":
                self.onPressFunction()
    
           
    def render(self, display):
        if self.hovering:
            border = makeRect(self.pos, self.size * 1.05)
            pygame.draw.rect(display, self.borderColor, border)
            pygame.draw.rect(display, self.color, self.rect)
        else:
            pygame.draw.rect(display, self.color, self.rect)
        
        if self.font and self.text:
            text = self.font.render(self.text, True, self.textColor)
            display.blit(text, (self.rect.left, self.rect.top))

class Dragable(Entity):
    def __init__(self, game, pos, size, eType, snapRects):
        super().__init__(game, pos, size, eType)
        self.relativeMousePos = None    
        self.snapRects = snapRects
        self.hasSnaped = False
    
    def snapToCenter(self):
        for sRect in self.snapRects:
            if self.getRect().colliderect(sRect.rect):
                self.setPos(sRect.pos)
                self.hasSnaped = True
                if sRect.occupant and not sRect.occupant == self:
                    sRect.occupant.hasSnaped = False
                sRect.occupant = self
                break
    def onPress(self, mousePos):
        self.getRelativeMousePos(mousePos)
        self.hasSnaped = False
        print(f"center: {self.pos}, mouse pos: {mousePos}")
    
    def getRelativeMousePos(self, mousePos):
        self.relativeMousePos = pygame.Vector2(self.pos) - pygame.Vector2(mousePos) + self.size/2
    def update(self):
        self.wasPressed = False
        self.velocity += self.acceleration
        self.velocity *= self.friction
        if self.hasSnaped:
            self.setVelocity((0, 0))
        self.move(self.velocity, self.platforms)
        self.checkIfPressed()
        if len(self.game.textEvent) > 0:
            self.handleTextEvents(self.game.textEvent)
        
class Rob(Entity):
    def __init__(self, game, pos, size):
        super().__init__(game, pos, size, "rob")
    
    def handleTextEvents(self, events):
        for event in events:
            if event in self.images:
                self.setImage(event)
    
    
