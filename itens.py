import pygame

class Itens:
    def __init__(self, win, x, y, w, h, img, r):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.win = win
        self.visible = True
        self.mask = None

        # Inicializa _img e _r antes de chamar os setters
        self._img = img
        self._r = r

        # chama os setters
        self.img = img  # Esta linha vai chamar update_transformations
        self.r = r      # Esta linha também vai chamar update_transformations

    @property
    def r(self):
        return self._r

    @r.setter
    def r(self, value):
        self._r = value
        self.update_transformations()

    @property
    def img(self):
        return self._img

    @img.setter
    def img(self, value):
        self._img = value
        self.update_transformations()    

    def update_transformations(self):
        if self._img is not None and self._r is not None:
            self.transformed_img = pygame.transform.rotate(self.img, self.r)
            self.transformed_img = pygame.transform.scale(self.transformed_img, (self.w, self.h))
            self.mask = pygame.mask.from_surface(self.transformed_img)

    def show(self):
        if self.visible:
            self.win.blit(self.transformed_img, (self.x, self.y))
