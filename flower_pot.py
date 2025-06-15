from assets import *
from grid_object import *

class flower_pot(Grid_Object):
    def __init__(self, grid_position, image, tile_size , is_blocked=None, collidable=True):
        super().__init__(grid_position, image, tile_size, is_blocked,collidable=collidable)

        self.harvested = False

    def harvest(self):
        self.original_image = PLANT_HARVESTED
        self.resize(self.tile_size)
        self.harvested = True
