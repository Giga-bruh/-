import pygame as pg
class Npc(pg.sprite.Sprite):
    def __init__(self,x,y,sprite_animation_idle,num_idle):
        super().__init__()
        self.sprite_animation_idle = sprite_animation_idle
        self.num_idle = num_idle
        self.load_animation()
        self.image=self.animation[0]

        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y


        self.current_image=0
        self.interval = 200
        self.timer = pg.time.get_ticks()







    def load_animation(self):
        tile_size = 32
        tile_scale = 4
        self.animation = []
        num_im=self.num_idle

        spritesheet_idle = pg.image.load(self.sprite_animation_idle)
        for i in range(num_im):
            x = i * tile_size
            y = 0
            rect = pg.Rect(x, y, tile_size, tile_size)
            image = spritesheet_idle.subsurface(rect)
            image = pg.transform.scale(image, (tile_size * tile_scale, tile_size * tile_scale))
            self.animation.append(image)
        self.animation=[pg.transform.flip(image, True, False)
        for image in self.animation]

    def update(self):

        if pg.time.get_ticks() - self.timer>self.interval:
            self.current_image+=1

            if self.current_image>=len(self.animation):

                self.current_image=0
            self.image=self.animation[self.current_image]
            self.timer=pg.time.get_ticks()
