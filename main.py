import pygame as pg
import pytmx
import Player
pg.init()

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600
FPS = 80
TILE_SCALE=2

class Platforma(pg.sprite.Sprite):
    def __init__(self,image,x,y,width,height):
        super(Platforma,self).__init__()

        self.image=pg.transform.scale(image,(width*TILE_SCALE,height*TILE_SCALE))
        self.rect=self.image.get_rect()
        self.rect.x=x*TILE_SCALE
        self.rect.y=y*TILE_SCALE

class Game:
    def __init__(self):
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pg.display.set_caption("Платформер")

        self.clock = pg.time.Clock()


        self.is_running = False
        self.all_sprites=pg.sprite.Group()
        self.platforms=pg.sprite.Group()
        self.tmx_map=pytmx.load_pygame("level2.tmx")
        self.map_width=self.tmx_map.width*self.tmx_map.tilewidth*TILE_SCALE

        self.map_height=self.tmx_map.height*self.tmx_map.tileheight*TILE_SCALE
        self.player=Player.Player(self.map_width,self.map_height)
        self.all_sprites.add(self.player)
        for a in self.tmx_map:
            for x,y,gid in a:

                tile=self.tmx_map.get_tile_image_by_gid(gid)

                if tile:
                    platformi=Platforma(tile,x*self.tmx_map.tilewidth,y*self.tmx_map.tileheight,self.tmx_map.tilewidth,self.tmx_map.tileheight)
                    self.all_sprites.add(platformi)
                    self.platforms.add(platformi)


        self.camera_x = 0
        self.camera_y = 0
        self.camera_speed = 4
        self.run()

    def run(self):
        self.is_running = True
        while self.is_running:
            self.event()
            self.update()
            self.draw()
            self.clock.tick(60)
        pg.quit()
        quit()

    def event(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.is_running = False


    def update(self):

        self.player.update(self.platforms)


        self.camera_x=self.player.rect.x-SCREEN_WIDTH//2

        self.camera_y = self.player.rect.y - SCREEN_HEIGHT // 2
        self.camera_x=max(0,min(self.camera_x,self.map_width-SCREEN_WIDTH))
        self.camera_y = max(0, min(self.camera_y, self.map_height - SCREEN_HEIGHT))

    def draw(self):
        self.screen.fill("light blue")



        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, sprite.rect.move(-self.camera_x, -self.camera_y))
        pg.display.flip()


if __name__ == "__main__":
    game = Game()