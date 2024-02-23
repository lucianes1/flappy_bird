import pygame
import os
import random
import itens
from pygame.locals import *

width, height = 800, 600
gover = True
cair = False
game = True
cano = []
mover = 1
vel_y = 0
speed = 4

pygame.init()
win = pygame.display.set_mode((width, height))
bird0 = pygame.image.load("imgs/bird1.png")
bird1 = pygame.image.load("imgs/bird2.png")
bird2 = pygame.image.load("imgs/bird3.png")
piso = pygame.image.load("imgs/base.png")
tubo = pygame.image.load("imgs/tubo.png")
cena = pygame.image.load("imgs/fundo.png")
asas = 0
pts = 0

ply = itens.Itens(win, 200, height / 2, 50, 50, bird0, 0)
fundo0 = itens.Itens(win, 0, 210, width, height, cena, 0)
fundo1 = itens.Itens(win, width, 210, width, height, cena, 0)
piso0 = itens.Itens(win, 0, height - 50, width, 112, piso, 0)
piso1 = itens.Itens(win, width, height - 50, width, 112, piso, 0)

for i in range(2):
    cano.append([0] * 4)

for i in range(4):
    cano[0][i] = itens.Itens(win, i * 210, -100, 87, 310, tubo, 0)
    cano[1][i] = itens.Itens(win, i * 210, 400, 87, 310, tubo, 0)

def restart():
    global vel_y, speed, cair, pts

    for i in range(4):
        cano[0][i].x = width + i * 220
        cano[1][i].x = width + i * 220
        visible = random.randint(0, 1)
        cano[0][i].visible = visible
        cano[1][i].visible = visible
        canoy = random.randint(0, 9) * -(cano[0][0].h/12)
        cano[0][i].y = canoy
        cano[1][i].y = canoy + 470
        cano[1][i].r = 180

    ply.y = height/3
    vel_y = 0
    cair = False
    pts = 0
    

def paint():
    pygame.display.update()
    pygame.time.delay(10)
    win.fill(0x3C2EE)
    
    move_fundo()
    
    move_cano()
    move_piso()
    move_ply()

def move_cano():
    for i in range(4):
        cano[0][i].show()
        cano[1][i].show()
        cano[0][i].x -= mover * speed
        cano[1][i].x -= mover * speed

        if(cano[0][i].x < -cano[0][0].w):
            visible = random.randint(0, 1)
            cano[0][i].visible = visible
            cano[1][i].visible = visible
            canoy = random.randint(0, 9) * -(cano[0][0].h/12)
            cano[0][i].y = canoy
            cano[1][i].y = canoy + 470
            cano[0][i].x = width
            cano[1][i].x = width

def move_ply():
    global asas
    ply.show()

    asas += 1
    if asas < 5:
        ply.img = bird0
    elif asas < 10:
        ply.img = bird1
    else: 
        ply.img = bird2

    if asas > 15:
        asas = 0

def move_fundo():
    if (fundo0.x < -width):
        fundo0.x = 0
        fundo1.x = width

    fundo0.x -= mover * 1
    fundo1.x -= mover * 1

    fundo0.show()
    fundo1.show()

def move_piso():
    if (piso0.x < -width):
        piso0.x = 0
        piso1.x = width

    piso0.x -= mover * 5
    piso1.x -= mover * 5
    
    piso0.show()
    piso1.show()

def check_collision(item1, item2):
    offset_x = item2.x - item1.x
    offset_y = item2.y - item1.y
    return item1.mask.overlap(item2.mask, (offset_x, offset_y)) is not None

def control():
    global gover, vel_y, mover, cair
    mover = not gover

    vel_y += mover
    ply.y += vel_y
    ply.r = mover * (-vel_y) * 3

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            return False
        if event.type == KEYDOWN and event.key == K_SPACE and gover:              
            gover = False
            restart()
        if event.type == pygame.MOUSEBUTTONDOWN and not cair:
            vel_y = mover * -12  

    return True

def jogo():
    global gover, mover, asas, cair, pts, top

    #Perdendo
    for i in range(2):
        for j in range(4):
            if (check_collision(cano[i][j], ply) and cano[i][j].visible):
                cair = True
            if not i and 200 < cano[i][j].x < 205 and cano[i][j].visible and not gover:
                pts += 1
                if ply.y < cano[i][j].y:
                    cair = True
    if ply.y > piso0.y - ply.h:
        gover = True
        ply.r = -90
        asas = 0
        cair = True                    

while game:
    jogo()
    paint()
    game = control()



