import pygame 
import textwrap

class Textbox:
    #textboxen ska rita upp texten
    def __init__(self, pos, duration, font = None):
        self.text = ""
        self.duration = duration
        self.done = False
        self.char = 0
        self.color = (0,0,255)
        self.font = font
        self.pos = pos
        self.width = 400
        self.height = 110
        
        self.textRect = pygame.Rect(self.pos[0],self.pos[1],self.width,self.height)
    def setText(self, text):
        self.text = text
    def copy(self):
        return Textbox(self.pos,self.text,self.duration)
    
    def update(self):
        self.char = min(self.char + 1, self.duration * len(self.text))
        if self.char >= self.duration * len(self.text)-1:
            self.done = True

    def sayText(self):
        return self.text[0:min(self.char//self.duration,len(self.text))]
    
    def drawText(self,display):
        saidText = self.sayText()
        pygame.draw.rect(display,(0,0,0), self.textRect)

        yOffset = 0
        xOffset = 0

        y_offset = self.textRect.top
        wrapped_text = textwrap.wrap(saidText,60)
        #screen.blit(self.baseImage,self.rect)
        #screen.blit(self.characterImage,self.characterRect)
        for line in wrapped_text:
            text = self.font.render(line, True, self.color)
            display.blit(text, (self.textRect.left, y_offset))
            y_offset += text.get_height()
            