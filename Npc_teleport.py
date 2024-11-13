import pygame as pg
import npc
class Npc_teleport(npc.Npc):
    def __init__(self,x,y,sprite_animation_idle,num_idle):
        super().__init__(x,y,sprite_animation_idle,num_idle)
        self.num_idle = num_idle
    def load_animation(self):
        super().load_animation()
        num_im=self.num_idle

    def update(self):
        super().update()