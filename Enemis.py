import pygame as pg
import Player
import main
from main import *
TILE_SCALE=2
class Enemis(pg.sprite.Sprite):
    def __init__(self, map_width, map_height,player,start_pos,final_pos):
        super(Enemis, self).__init__()
        self.load_animation()
        self.current_animation=self.idle_animation_right
        self.image=self.current_animation[0]
        self.current_image=0

        self.rect = self.image.get_rect()
        self.rect.bottomleft=start_pos
        self.igrok=player

        self.velocity_x = 0
        self.velocity_y = 0
        self.gravity = 2
        self.right_edge=final_pos[0]+self.image.get_width()

        self.left_edge=start_pos[0]
        self.is_jumping = False
        self.map_width = map_width * TILE_SCALE
        self.map_height = map_height * TILE_SCALE
        self.timer=pg.time.get_ticks()
        self.interval=200
        self.direction="right"
        self.idet_za_igrokom=0
        print(self.rect.x)
    def load_animation(self):
        tile_size = 32
        tile_scale = 4
        self.idle_animation_right = []
        self.run_animation_right=[]
        num_im = 1
        spritesheet_idle = pg.image.load("Sprite Pack 5/1 - Robo Retro/Pilot_Idle_(32 x 32).png")
        spritesheet_run=pg.image.load("Sprite Pack 5/1 - Robo Retro/Pilot_Running_(32 x 32).png")
        for i in range(num_im):
            x = i * tile_size
            y = 0
            rect = pg.Rect(x, y, tile_size, tile_size)
            image = spritesheet_idle.subsurface(rect)
            image = pg.transform.scale(image, (tile_size * tile_scale, tile_size * tile_scale))
            self.idle_animation_right.append(image)
        self.idle_animation_left = [pg.transform.flip(image, True, False) for image in self.idle_animation_right]
        num_im=3
        for i in range(num_im):
            x = i * tile_size
            y = 0
            rect = pg.Rect(x, y, tile_size, tile_size)
            image = spritesheet_run.subsurface(rect)
            image = pg.transform.scale(image, (tile_size * tile_scale, tile_size * tile_scale))
            self.run_animation_right.append(image)
        self.run_animation_left = [pg.transform.flip(image, True, False) for image in self.run_animation_right]

    def update(self, platforms):

        if self.direction=="right" and self.idet_za_igrokom==0:
            self.velocity_x=10
            if self.rect.right>=self.right_edge:
                self.direction="left"

        elif self.direction == "left" and self.idet_za_igrokom == 0:
            self.velocity_x = -10
            if self.rect.left <= self.left_edge:
                self.direction = "right"






        if self.igrok.rect.x - self.rect.x <= 50 and self.rect.y==self.igrok.rect.y:
            self.idet_za_igrokom=1
            if self.current_animation!=self.run_animation_left:
                self.current_animation=self.run_animation_left
                self.current_image=0

            self.velocity_x=-7

        elif self.rect.x - self.igrok.rect.x <= 50 and self.rect.y==self.igrok.rect.y:
            self.idet_za_igrokom=1
            if self.current_animation!=self.run_animation_right:
                self.current_animation=self.run_animation_right
                self.current_image=0

            self.velocity_x =7


        else:
            if self.current_animation == self.run_animation_right:
                self.current_animation=self.idle_animation_right
                self.current_image=0

            elif self.current_animation == self.run_animation_left:
                self.current_animation = self.idle_animation_left
                self.current_image = 0
            # self.velocity_x=0

            self.idet_za_igrokom=0

        new_x = self.rect.x + self.velocity_x
        if 0 <= new_x <= self.map_width - self.rect.width:
            self.rect.x = new_x

        self.velocity_y+=self.gravity
        self.rect.y+=self.velocity_y

        for platform in platforms:
            if platform.rect.collidepoint(self.rect.midbottom):
                self.rect.bottom=platform.rect.top
                self.velocity_y=0
                self.is_jumping=False
            if platform.rect.collidepoint(self.rect.midtop):
                self.rect.top=platform.rect.bottom
                self.velocity_y=0
            if platform.rect.collidepoint(self.rect.midright):
                self.rect.right=platform.rect.left
            if platform.rect.collidepoint(self.rect.midleft):
                self.rect.left=platform.rect.right

        if pg.time.get_ticks()-self.timer>self.interval:
            self.current_image+=1
            if self.current_image>=len(self.current_animation):
                self.current_image=0
            self.image=self.current_animation[self.current_image]
            self.timer=pg.time.get_ticks()

