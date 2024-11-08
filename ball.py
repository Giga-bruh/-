import pygame as pg
class Ball(pg.sprite.Sprite):
    def __init__(self, player_rect, direction):
        super(Ball, self).__init__()

        self.direction = direction
        self.speed = 10

        self.image = pg.image.load("шар.png")
        self.image = pg.transform.scale(self.image, (30, 30))

        self.stolkneylsa_s_stenoi=False

        self.palyer_rect=player_rect.rect

        self.rect = self.image.get_rect()

        self.rect.y=self.palyer_rect.centery
        if self.direction=="right":
            self.rect.x=self.palyer_rect.right
        else:
            self.rect.x=self.palyer_rect.left
        self.velocity_x = 0
        self.velocity_y = 0

    def update(self,platforms):

        if self.direction=="right":
            self.rect.x+=self.speed
        if self.direction == "left":
            self.rect.x -= self.speed

        for platform in platforms:
            if platform.rect.collidepoint(self.rect.midbottom):
                self.stolkneylsa_s_stenoi=True
            if platform.rect.collidepoint(self.rect.midtop):
                self.stolkneylsa_s_stenoi=True
            if platform.rect.collidepoint(self.rect.midright):
               self.stolkneylsa_s_stenoi=True
            if platform.rect.collidepoint(self.rect.midleft):
                self.stolkneylsa_s_stenoi=True

