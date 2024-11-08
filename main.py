import json
import ball
import pygame as pg
import pytmx
import Player
import Coins
import Enemis
pg.init()

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600
FPS = 80
TILE_SCALE=2
font=pg.font.Font(None,36)

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
        self.setup()
    #noinspection PyAttributeOutsideInit
    def setup(self):
        self.gamemode="game"
        self.clock = pg.time.Clock()


        self.is_running = False
        self.colected_coins=0
        self.all_sprites=pg.sprite.Group()
        self.platforms=pg.sprite.Group()
        self.enemis = pg.sprite.Group()
        self.shar=pg.sprite.Group()
        self.coins=pg.sprite.Group()
        self.tmx_map=pytmx.load_pygame("level2.tmx")
        self.map_width=self.tmx_map.width*self.tmx_map.tilewidth*TILE_SCALE


        self.map_height=self.tmx_map.height*self.tmx_map.tileheight*TILE_SCALE
        self.player=Player.Player(self.map_width,self.map_height)

        self.all_sprites.add(self.player)
        for a in self.tmx_map:
            if a.name=="platforms":
                for x,y,gid in a:

                    tile=self.tmx_map.get_tile_image_by_gid(gid)

                    if tile:
                        platformi=Platforma(tile,x*self.tmx_map.tilewidth,y*self.tmx_map.tileheight,self.tmx_map.tilewidth,self.tmx_map.tileheight)
                        self.all_sprites.add(platformi)
                        self.platforms.add(platformi)
            elif a.name == "coins":
                for x, y, gid in a:

                    tile = self.tmx_map.get_tile_image_by_gid(gid)

                    if tile:
                        coin = Coins.Coin( x * self.tmx_map.tilewidth * TILE_SCALE, y * self.tmx_map.tileheight*TILE_SCALE)
                        self.all_sprites.add(coin)
                        self.coins.add(coin)
        with open("level1_enemis.json","r") as json_file:
            data=json.load(json_file)
            print(data)


        for enemy in data["enemis"]:
            if enemy["Name"]=='Bomb':
                x1=enemy["start_pos"][0] * TILE_SCALE * self.tmx_map.tilewidth
                y1 = enemy["start_pos"][1] * TILE_SCALE * self.tmx_map.tilewidth

                x2 = enemy["final_pos"][0] * TILE_SCALE * self.tmx_map.tilewidth
                y2 = enemy["final_pos"][1] * TILE_SCALE * self.tmx_map.tilewidth
                print("a")
                bomba=Enemis.Enemis(self.map_width,self.map_height,self.player,[x1,y1],[x2,y2])
                self.enemis.add(bomba)
                self.all_sprites.add(bomba)
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
            if self.gamemode=="game over":
                if event.type==pg.KEYDOWN:
                    self.setup()

            if event.type == pg.KEYDOWN:

                keys = pg.key.get_pressed()
                if keys[pg.K_q]:

                        bil=ball.Ball(self.player,self.player.direction)
                        self.shar.add(bil)
                        self.all_sprites.add(bil)

    def update(self):
        if self.player.hp<=0:
            self.gamemode="game over"
            return
        for enemy in self.enemis.sprites():
            if pg.sprite.collide_mask(self.player,enemy):
                self.player.get_damage()
            for ball in self.shar.sprites():
                if enemy.rect.colliderect(ball.rect):
                    self.shar.remove(ball)
                    self.all_sprites.remove(ball)
                    self.enemis.remove(enemy)
                    self.all_sprites.remove(enemy)
        for ball in self.shar.sprites():
            if ball.stolkneylsa_s_stenoi==True:
                self.shar.remove(ball)
                self.all_sprites.remove(ball)
            else:
                ball.update(self.platforms)
        for coin in self.coins.sprites():
            hints=pg.sprite.spritecollide(self.player,self.coins,True)
            for hint in hints:
                self.colected_coins+=1
            coin.update()




        self.player.update(self.platforms)
        for enemy in self.enemis.sprites():
            enemy.update(self.platforms)


        self.camera_x=self.player.rect.x-SCREEN_WIDTH//2

        self.camera_y = self.player.rect.y - SCREEN_HEIGHT // 2
        self.camera_x=max(0,min(self.camera_x,self.map_width-SCREEN_WIDTH))
        self.camera_y = max(0, min(self.camera_y, self.map_height - SCREEN_HEIGHT))

    def draw(self):
        self.screen.fill("light blue")



        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, sprite.rect.move(-self.camera_x, -self.camera_y))
        pg.draw.rect(self.screen, pg.Color("red"),(pg.rect.Rect([680,30],[self.player.hp*20,50])))

        pg.draw.rect(self.screen, pg.Color("black"),(pg.rect.Rect([680,30],[200,50])), 1)
        if self.gamemode=="game over":
            text= font.render("Вы проиграли",True,(255,0,0))
            text_rect=text.get_rect(center=(SCREEN_WIDTH//2,SCREEN_HEIGHT//2))
            self.screen.blit(text,text_rect)
        pg.display.flip()


if __name__ == "__main__":
    game = Game()