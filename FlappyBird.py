import pygame
import os
import random
import itens
from pygame.locals import *

width, height = 500, 800
gover = True
cair = False
game = True
mover = 1
vel_y = 0

pygame.init()
win = pygame.display.set_mode((width, height))
bird0 = pygame.image.load("imgs/bird1.png")
bird1 = pygame.image.load("imgs/bird2.png")
bird2 = pygame.image.load("imgs/bird3.png")
piso = pygame.image.load("imgs/base.png")
tubo = pygame.image.load("imgs/pipe.png")
cena = pygame.image.load("imgs/bg.png")
asas = 0

ply = itens.Itens(win, 200, height / 2, 34, 24, bird0, 0)
fundo0 = itens.Itens(win, 0, 0, width, height, cena, 0)
fundo1 = itens.Itens(win, width, 0, width, height, cena, 0)
piso0 = itens.Itens(win, 0, height - 50, width, 112, piso, 0)
piso1 = itens.Itens(win, width, height - 50, width, 112, piso, 0)


def paint():
    pygame.display.update()
    pygame.time.delay(10)
    win.fill(0x3C2EE)
    
    move_fundo()
    move_piso()
    move_ply()
  

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
    global gover

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            return False
    return True

while game:
    paint()
    game = control()



