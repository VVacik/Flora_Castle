import pygame
from Settings import *
from grid_object import Grid_Object
from assets import *

direction_map = {0: "front", 1: "back", 2: "left", 3: "right"}
directions = {1: (0, -1), 0: (0, 1), 2: (-1, 0), 3: (1, 0)}

class Player(Grid_Object):
    def __init__(self,grid_position, tile_size, image, is_blocked = None, collidable = True, movable_objects_group = None):
        super().__init__(grid_position, tile_size, image, is_blocked, collidable)

        #Obiekty na planszy które gracz może złapać
        self.movable_objects_group = movable_objects_group
        self.held_object = None

        #Parametry dodatkowe:
        self.facing = 0
        self.energy = 100


        self.images = {
            "front": PLAYER_IMG_FRONT,
            "back": PLAYER_IMG_BACK,
            "left": PLAYER_IMG_LEFT,
            "right": PLAYER_IMG_RIGHT,
        }

    def update_sprite_direction(self):
        direction = direction_map.get(self.facing, "front")
        self.original_image = self.images[direction]
        self.resize(self.tile_size)


    def handle_event(self, event):
        if event.type != pygame.KEYDOWN:
            return

        key_to_facing = {
            pygame.K_w: 1, pygame.K_UP: 1,
            pygame.K_s: 0, pygame.K_DOWN: 0,
            pygame.K_a: 2, pygame.K_LEFT: 2,
            pygame.K_d: 3, pygame.K_RIGHT: 3,
        }

        if event.key in key_to_facing:
            print(event.key)
            self.facing = key_to_facing[event.key]
            self.update_sprite_direction()
            if not self.animating:
                dx, dy = directions[self.facing]
                self.move(dx, dy)



    def move(self, dx, dy):
        print("moving")

        if self.animating:
            return
        new_player_x = self.grid_x + dx
        new_player_y = self.grid_y + dy

        if (
            0<= new_player_x < self.screen_w and
            0 <= new_player_y < self.screen_h):
                self.animated_move(dx, dy)


