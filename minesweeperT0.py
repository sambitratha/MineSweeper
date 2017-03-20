import pygame
import pygame.locals as locals
import random
import sys
import time


WINDOWLENGTH = 800
WINDOWHEIGHT = 800
BLACK = (0, 0, 0)
WHITE  = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
GREY = (128, 128, 128)

pygame.init()
DISPLAYSURF = pygame.display.set_mode((WINDOWLENGTH,WINDOWHEIGHT), 0, 32)
pygame.display.set_caption('Mine Sweeper!')
FPS = 60
fpsClock = pygame.time.Clock()
BOARDX = 20
BOARDY = 15
ROWS = BOARDY
COLS = BOARDX
MARGIN  = 2
XMARGIN = 50
YMARGIN = 50
GAMEOVER = False
MINENUMBER = 34
isDiscovered = [False] * (BOARDX*BOARDY)
isFlagged = [False] * (BOARDX*BOARDY)
isMine = None
font = pygame.font.Font("EraserRegular.ttf",24)
BOXWIDTH  = ((WINDOWLENGTH - 2*XMARGIN)/BOARDY) - MARGIN
BOXHEIGHT = ((WINDOWHEIGHT - 2*YMARGIN)/BOARDX) - MARGIN
mouseposx = 0
mouseposy = 0
touchable = True
rem_mines = MINENUMBER




def ifWon():
    rs = True
    for i in range(BOARDX*BOARDY):
        if not isDiscovered[i] and not isFlagged[i]:
            rs = False
            break
    return rs

def render_gameover():
    tObject, tRect = getStringObject("GAME OVER You win!!",WINDOWLENGTH/2 -10,WINDOWHEIGHT/2)
    DISPLAYSURF.blit(tObject, tRect)

def getStringObject(s,centerx,centery):
    COLOR = RED
    textObj = font.render(s,True,RED,GREEN)
    textRect = textObj.get_rect()
    textRect.center = (centerx, centery)
    return textObj , textRect

def showMineNumber():
    s = "remaining mines: "+str(rem_mines)
    textObj = font.render(s,True,RED,WHITE)
    textRect = textObj.get_rect()
    textRect.center = (200, 20)
    DISPLAYSURF.blit(textObj, textRect)

def drawBox(i,j):
    COLOR = GREY
    x_pos = XMARGIN + (BOXWIDTH + MARGIN)*i
    y_pos = YMARGIN + (BOXHEIGHT + MARGIN)*j
    if isDiscovered[i*BOARDX + j]:
        COLOR = GREEN
    if isFlagged[i*BOARDX + j]:
        COLOR = BLACK

    pygame.draw.rect(DISPLAYSURF,COLOR,(x_pos,y_pos,BOXWIDTH,BOXHEIGHT))
    if isDiscovered[i*BOARDX + j] and getNumberOfMines(i,j) !=  0:
        tObject, tRect = getStringObject(str(getNumberOfMines(i,j)), x_pos + int(BOXWIDTH/2) , y_pos + int(BOXHEIGHT/2))
        DISPLAYSURF.blit(tObject, tRect)



def drawMines(i,j):

    center_X = XMARGIN + (BOXWIDTH + MARGIN)*i + BOXWIDTH/2
    center_Y = YMARGIN + (BOXHEIGHT + MARGIN)*j + BOXHEIGHT/2
    RADIUS = int( min(BOXHEIGHT,BOXWIDTH) * 0.3)
    pygame.draw.circle(DISPLAYSURF,BLACK,(center_X,center_Y),RADIUS)

def drawFlag(i,j):

    x_pos = XMARGIN + (BOXWIDTH + MARGIN)*i
    y_pos = YMARGIN + (BOXHEIGHT + MARGIN)*j

    #add some codes here

def drawBoard(BOARDX,BOARDY):

    for i in range(ROWS):
        for j in range(COLS):

            drawBox(i,j)

            if GAMEOVER and isMine[i*BOARDX + j]:
                drawMines(i,j)


            if isFlagged[i*BOARDX + j]:
                drawFlag(i,j)

def generateBoard():
    li = [True]*MINENUMBER
    l = [False]* (BOARDX*BOARDY - MINENUMBER)
    li.extend(l)
    random.shuffle(li)
    return li

def getBoardNumber(posx,posy):

     x = (posx - XMARGIN) / (BOXWIDTH + MARGIN)
     y = (posy - YMARGIN) / (BOXHEIGHT + MARGIN)

     if x >= BOARDY or y >= BOARDX or x < 0 or y < 0:
        return -1 , -1
     return x , y

def ifMine(i,j):
    global isMine
    if i >= 0 and i < BOARDY and j >= 0 and j < BOARDX:
        return isMine[i*BOARDX + j]
    return False

def getNumberOfMines(i,j):
    rs = 0
    for k in range(3):
        if ifMine(i-1+k, j-1):
            rs += 1
        if ifMine(i-1+k, j+1):
            rs += 1

    if ifMine(i-1, j):
        rs += 1
    if ifMine(i+1, j):
        rs += 1

    return rs





def changeAllConsecutiveBoxOn(i,j):
    global isDiscovered
    c = 4
    #do smthng
    li= [[i,j]]
    top = 0
    while top != len(li) :

        if getNumberOfMines(li[top][0], li[top][1]) == 0:
            x, y = li[top][0], li[top][1]
            l = [[x, y+1], [x, y-1], [x-1, y-1], [x-1, y], [x-1, y+1], [x+1, y-1], [x+1, y], [x+1, y+1]]
            for index in range(8):
                if l[index][0] >=0 and l[index][0] < BOARDY and l[index][1] >= 0 and l[index][1] <BOARDX and l[index] not in li:
                    li.append(l[index])
                    isDiscovered[l[index][0]*BOARDX + l[index][1]] = True

        top +=1
        c -= 1





def main():
    global isFlagged , isDiscovered, isMine, mouseposx, mouseposy, GAMEOVER, touchable, rem_mines
    isMine = generateBoard()
    while True:
        DISPLAYSURF.fill(WHITE)
        if not ifWon():
            drawBoard(BOARDX,BOARDY)
            showMineNumber()
        else:
            render_gameover()
            print "over"
        for event in pygame.event.get():

            if event.type == locals.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == locals.KEYUP and touchable:
                print "entered"
                x , y = getBoardNumber(mouseposx, mouseposy)
                if event.key == locals.K_LEFT and not isFlagged[x*BOARDX + y]:
                    isFlagged[x*BOARDX + y] = True
                    if isMine[x*BOARDX + y]:
                        rem_mines -= 1
                if event.key == locals.K_RIGHT and isFlagged[x*BOARDX + y]:
                    isFlagged[x*BOARDX + y] = False
                    if isMine[x*BOARDX + y]:
                        rem_mines += 1


            if event.type == locals.MOUSEBUTTONUP and touchable:
                x, y = getBoardNumber(mouseposx, mouseposy)
                isDiscovered[x * BOARDX + y ] = True
                if getNumberOfMines(x, y) == 0:
                    changeAllConsecutiveBoxOn(x, y)
                if ifMine(x, y):
                    GAMEOVER = True
                    touchable = False

            if event.type == locals.MOUSEMOTION:
                mouseposx, mouseposy = event.pos


        pygame.display.update()

main()








