import pygame
import textwrap
from utils import *
from random import randrange
from entity import *

class Game:
    def __init__(self, main, display):
        self.main = main
        self.window = display
        self.entities = []
        self.draging = None
        self.generalTimer = 0
        #RENDERLAYERS
        self.showTalkButtons = True
        self.rl0 = [] #bakgrunden
        self.rl1 = [] #lagret precis framför bakgrunden
        self.rl2 = [] 
        self.rl3 = [] 
        self.rl4 = [] # Vanligen robs lager
        self.rlDB = [] # DIalogknapparna
        self.rlUI = [] # lagret för UI
        #DIALOG OCH TEXTDISPLAY
        self.dialogText = None
        self.textRect = pygame.Rect(TEXBOX_X, TEXTBOX_Y, TEXTBOX_WIDTH, TEXTBOX_HEIGHT)
        self.activeTextIndex = 0
        self.textTimer = 0
        self.textSource = None
        self.textColor = (255,255,255)
        self.textDuration = 2
        self.textEvent = []
        self.textImage = "none"

        #SPELSCENERNA
        self.images = {}
        self.background = None
        self.firstLoop = True
        self.currentEvent = "start"
        self.subEvent = None
    def RLHeightInsert(self, object, rl):
        for i in range(len(rl)):
            if object.getImageRect().bottom < rl[i].getImageRect().bottom:
                rl.insert(i, object)
                return
        rl.append(object)
    def manageDraging(self):
        mousePos = pygame.mouse.get_pos()
        mouseDown = self.main.inputs["mouseDown"]
        #self.draging = None
                    
        if self.draging:
            self.draging.setVelocity((0, 0))
            if not self.draging.relativeMousePos:
                self.draging.relativeMousePos = (0, 0)
            self.draging.setPos(pygame.Vector2(mousePos) + self.draging.relativeMousePos) 
            if self.main.justUp == "mouse1":
                self.draging.snapToCenter()
                self.draging = None
            return
        
        for entity in self.entities:
            if isinstance(entity, Dragable):
                if entity.getImageRect().collidepoint(mousePos) and mouseDown:
                    self.draging = entity
                    if self.main.justPressed == "mouse1":
                        self.draging.getRelativeMousePos(mousePos)       
    
    def handleDialog(self, dialogList):
        if len(dialogList) > self.activeTextIndex:
            currenCharacter = self.textTimer //self.textDuration
            textData = dialogList[self.activeTextIndex]
            text = textData.text
            
            self.textSource = textData.source
            self.textColor = textData.color
            self.textDuration = textData.duration
            self.textEvent = textData.special
            self.textImage = textData.profile
            
            saidText = text[0:min(currenCharacter, len(text))]
            self.dialogText = textwrap.wrap(saidText,CHARACTER_PER_ROW)

            self.textTimer += 1
            
            if currenCharacter >= len(text) and "no wait" in self.textEvent:
                self.activeTextIndex += 1
                self.textTimer = 0
            
            if self.main.justPressed == "space":
                if currenCharacter < len(text):
                    self.textTimer = 100000000
                else:
                    self.activeTextIndex += 1
                    self.textTimer = 0
            return False
        else:
            self.dialogText = None 
            return True
             
        
    def updateAll(self):
        self.manageDraging()
        updateEntList(self.entities)   

    def renderDialog(self, wrapedText, display):
        pygame.draw.rect(display,(0,0,0), makeRect(self.textRect.center, (TEXTBOX_WIDTH + 10 * GAME_SCALE, TEXTBOX_HEIGHT + 20 * GAME_SCALE)))
        pygame.draw.rect(display,(0,0,0), self.textRect)
        display.blit(self.images["profiles"][self.textImage], (TEXBOX_X, TEXTBOX_Y))
        y_offset = self.textRect.top
        for line in wrapedText:
            text = self.fonts[self.textSource].render(line, True, self.textColor)
            display.blit(text, (self.textRect.left + 90 * GAME_SCALE, y_offset))
            y_offset += text.get_height()
        
    def renderAll(self):
        self.window.fill((0,0,0)) 
        if self.rl0:
            renderEntList(self.rl0, self.window)            
        renderEntList(self.rl1, self.window) 
        renderEntList(self.rl2, self.window)
        renderEntList(self.rl3, self.window)
        renderEntList(self.rl4, self.window)
        
        if self.showTalkButtons: renderEntList(self.rlDB, self.window)
        if self.dialogText: self.renderDialog(self.dialogText, self.window)
        if self.draging: self.draging.render(self.window)
            
        renderEntList(self.rlUI, self.window)    
        
    
    def run(self):
        
        self.events[self.currentEvent](self.firstLoop)
        self.updateAll()
        self.renderAll() 
        
        pygame.display.update()   

