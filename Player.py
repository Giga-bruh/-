import pygame as pg

from main import *
class Player(pg.sprite.Sprite):
    def __init__(self, map_width, map_height,x,y):
        super(Player, self).__init__()
        self.load_animation()
        self.current_animation=self.idle_animation_right
        self.image=self.current_animation[0]
        self.current_image=0

        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.x=x
        self.y=y

        self.direction="right"
        self.velocity_x = 0
        self.velocity_y = 0
        self.gravity = 2
        self.is_jumping = False
        self.map_width = map_width * TILE_SCALE
        self.map_height = map_height * TILE_SCALE
        self.timer=pg.time.get_ticks()
        self.interval=200
        self.hp = 10
        self.damage_timer = pg.time.get_ticks()
        self.damage_interval = 1000

    def load_animation(self):
        tile_size = 32
        tile_scale = 4

        self.idle_animation_right = []
        self.run_animation_right=[]
        num_im = 6
        spritesheet_idle = pg.image.load("Sprite Pack 5/3 - Big Red/Idle_(32 x 32).png")
        spritesheet_run=pg.image.load("Sprite Pack 5/3 - Big Red/Running_(32 x 32).png")
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

        keys = pg.key.get_pressed()
        if keys[pg.K_SPACE] and not self.is_jumping:
            self.jump()
        if keys[pg.K_a]:
            if self.current_animation!=self.run_animation_left:
                self.current_animation=self.run_animation_left
                self.current_image=0
                self.direction="left"

            self.velocity_x=-10

        elif keys[pg.K_d]:
            if self.current_animation!=self.run_animation_right:
                self.current_animation=self.run_animation_right
                self.current_image=0
                self.direction="right"

            self.velocity_x =10
        else:
            if self.current_animation == self.run_animation_right:
                self.current_animation=self.idle_animation_right
                self.current_image=0
            elif self.current_animation == self.run_animation_left:
                self.current_animation = self.idle_animation_left
                self.current_image = 0
            self.velocity_x=0


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
        if self.rect.y>SCREEN_HEIGHT*2.2:
            self.hp-=1
            self.rect.center = (self.x,self.y)

        if pg.time.get_ticks()-self.timer>self.interval:
            self.current_image+=1
            if self.current_image>=len(self.current_animation):
                self.current_image=0
            self.image=self.current_animation[self.current_image]
            self.timer=pg.time.get_ticks()




    def jump(self):
        self.velocity_y = -25
        self.is_jumping = True
    def get_damage(self):
        if pg.time.get_ticks()-self.damage_timer>self.damage_interval:
            self.hp -=1
            self.damage_timer=pg.time.get_ticks()