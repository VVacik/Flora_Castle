from grid_object import Grid_Object


class Not_movable_blockade(Grid_Object):
    def __init__(self, grid_position, image, tile_size,is_blocked=None, collidable=True,):
        super().__init__(grid_position, image, tile_size, is_blocked, collidable)
