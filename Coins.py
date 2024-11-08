import pygame as pg
class Coin(pg.sprite.Sprite):
    def __init__(self,x,y):
        super(Coin, self).__init__()


        self.load_animation()
        self.image=self.animation[0]

        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        self.current_image=0
        self.interval = 200
        self.timer = pg.time.get_ticks()







    def load_animation(self):
        tile_size = 10
        tile_scale = 4
        self.animation = []
        num_im=4
        spritesheet_idle = pg.image.load("4 Animated objects/Coin.png")
        for i in range(num_im):
            x = i * tile_size
            y = 0
            rect = pg.Rect(x, y, tile_size, tile_size)
            image = spritesheet_idle.subsurface(rect)
            image = pg.transform.scale(image, (tile_size * tile_scale, tile_size * tile_scale))
            self.animation.append(image)

    def update(self):

        if pg.time.get_ticks() - self.timer>self.interval:
            self.current_image+=1

            if self.current_image>=len(self.animation):

                self.current_image=0
            self.image=self.animation[self.current_image]
            self.timer=pg.time.get_ticks()
