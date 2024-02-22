import pygame

class Itens:
    def __init__(self, win, x, y, w, h, img, r):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.r = r
        self.visible = True
        self.img = img
        self.win = win
        self.mask = None
        self.update_transformations()


    @property
    def img(self):
        return self._img

    @img.setter
    def img(self, value):
        self._img = value
        self.update_transformations()    

    def update_transformations(self):
        self.transformed_img = pygame.transform.rotate(self.img, self.r)
        self.transformed_img = pygame.transform.scale(self.transformed_img, (self.w, self.h))
        

    def show(self):
        if self.visible:
            self.win.blit(self.transformed_img, (self.x, self.y))