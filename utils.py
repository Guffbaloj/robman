import pygame

BASE_PATH = "images/"
GAME_SCALE = 1
WIDTH = 640 * GAME_SCALE 
HEIGHT = 480 * GAME_SCALE
CENTER_POS = pygame.math.Vector2(WIDTH/2,HEIGHT/2)
FPS = 60

TEXT_SIZE = 25 * GAME_SCALE
TEXTBOX_WIDTH = 500 * GAME_SCALE
TEXTBOX_HEIGHT = 100 * GAME_SCALE
TEXBOX_X = WIDTH/2 - TEXTBOX_WIDTH/2
TEXTBOX_Y = HEIGHT - TEXTBOX_HEIGHT - 80 * GAME_SCALE
CHARACTER_PER_ROW = 60

#Spelpunkter
X_POINT = WIDTH // 200
Y_POINT = HEIGHT // 200

def scaledPos(x, y):
    return [x * GAME_SCALE, y * GAME_SCALE]

def loadImage(path, size = 1):
    image = pygame.image.load(BASE_PATH+path)
    height, width = image.get_size()
    image = pygame.transform.scale(image,(height*size * GAME_SCALE, width*size * GAME_SCALE))
    image.convert()
    image.set_colorkey((0,0,0))
    return image

def pygameQuitEvent():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

def makeRect(centerPos, size):
    rect = pygame.rect.Rect(0, 0, size[0], size[1])
    rect.center = centerPos
    return rect

def updateEntList(list):
    for item in list:
        item.update()
def renderEntList(list, display):
    for item in list:
        item.render(display)