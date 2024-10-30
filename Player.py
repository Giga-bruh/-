import pygame as pg

from main import *
class Player(pg.sprite.Sprite):
    def __init__(self, map_width, map_height):
        super(Player, self).__init__()

        self.image = pg.Surface((50,50))
        self.image.fill("red")

        self.rect = self.image.get_rect()
        self.rect.center = (200, 100)


        self.velocity_x = 0
        self.velocity_y = 0
        self.gravity = 2
        self.is_jumping = False
        self.map_width = map_width * TILE_SCALE
        self.map_height = map_height * TILE_SCALE

    def update(self, platforms):
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.velocity_x=-10

        elif keys[pg.K_d]:
            self.velocity_x =10
        else:
            self.velocity_x=0
        self.velocity_y+=self.gravity
        self.rect.y+=self.velocity_y
        for platform in platforms:
            if platform.rect.collidepoint(self.rect.midbottom):
                self.rect.bottom=platform.rect.top
                self.velocity_y=0
            if platform.rect.collidepoint(self.rect.midtop):
                self.rect.top=platform.rect.bottom
                self.velocity_y=0

        new_x = self.rect.x + self.velocity_x
        if 0 <= new_x <= self.map_width - self.rect.width:
            self.rect.x = new_x
