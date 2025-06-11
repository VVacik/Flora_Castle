import pygame
from grid_object import Grid_Object

from Settings import *


class Movable_Object(Grid_Object):
    def __init__(self, grid_position, image, tile_size,is_blocked =None, collidable=True,):
        super().__init__(grid_position, image, tile_size, is_blocked,collidable=collidable)

        self.throw_path = []




    def update(self, dt):
        super().update(dt)

        if not self.animating and self.throw_path:
            next_x, next_y = self.throw_path.pop(0)
            self.animated_move(next_x -self.grid_x, next_y - self.grid_y)
