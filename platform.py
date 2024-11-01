import pygame as pg
import pytmx

from main import *
class Platforma(pg.sprite.Sprite):
    def __init__(self,image,x,y,width,height):
        super(Platforma,self).__init__()
        self.image=pg.transform.scale(width*TILE_SCALE,height*TILE_SCALE)
        self.rect=self.image.get_rect()
        self.rect.x=x*TILE_SCALE
        self.rect.y=y*TILE_SCALE
