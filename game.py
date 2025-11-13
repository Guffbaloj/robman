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

        #DIALOG OCH TEXTDISPLAY
        self.dialogText = None
        self.textRect = pygame.Rect(TEXBOX_X, TEXTBOX_Y, TEXTBOX_WIDTH, TEXTBOX_HEIGHT)
        self.activeTextIndex = 0
        self.textTimer = 0
        self.textSource = None
        self.textColor = (255,255,255)
        self.textDuration = 2

        #SPELSCENERNA
        self.images = {}
        self.background = None
        self.firstLoop = True
        self.currentEvent = "start"
        
            
    def updateEntList(self,list):
        for item in list:
            item.update()
    def renderEntList(self, list, display):
        for item in list:
            if not item == self.draging:
                item.render(display)
        if self.draging:
            self.draging.render(self.window)
    
    def manageDraging(self):
        mousePos = pygame.mouse.get_pos()
        mouseDown = self.main.inputs["mouseDown"]
        #self.draging = None
                    
        if self.draging:
            
            self.draging.setPos((mousePos[0] + self.draging.relativeMousePos.x, mousePos[1] + self.draging.relativeMousePos.y)) 
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
            text = textData["text"]
            
            self.textSource = None
            self.textColor = (255,255,255)
            self.textDuration = 2
            try: self.textSource = textData["source"]
            except:
                pass
            try: self.textColor = textData["color"]
            except:
                pass
            try: self.textDuration = textData["speed"]
            except:
                pass
            
            saidText = text[0:min(currenCharacter, len(text))]
            self.dialogText = textwrap.wrap(saidText,CHARACTER_PER_ROW)

            self.textTimer += 1
            
            if self.main.justPressed == "space":
                if currenCharacter < len(text):
                    self.textTimer = 100000000
                else:
                    self.activeTextIndex += 1
                    self.textTimer = 0
        else:
            self.activeTextIndex = "Done"
            self.dialogText = None
        
    def updateAll(self):
        self.manageDraging()
        self.updateEntList(self.entities)   

    def renderDialog(self, wrapedText, display):
        pygame.draw.rect(display,(0,0,0), self.textRect)
        y_offset = self.textRect.top
        for line in wrapedText:
            text = self.fonts[self.textSource].render(line, True, self.textColor)
            display.blit(text, (self.textRect.left, y_offset))
            y_offset += text.get_height()
        
    def renderAll(self):
        
        #Faktiska spelet
        self.renderEntList(self.entities, self.window)
        if self.draging:
            self.draging.render(self.window)
        if self.dialogText:
            self.renderDialog(self.dialogText, self.window)
    
    def run(self):
        if not self.background: 
            self.window.fill((255,255,255))    
        else: 
            self.window.blit(self.images[self.background], (0,0))
        self.events[self.currentEvent](self.firstLoop)
        self.updateAll()
        self.renderAll() 
            
        pygame.display.update()   

