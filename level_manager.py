from assets import *
import pygame
from room import Room


class LevelManager:
    def __init__(self):
        self.rooms = {}
        self.current_room = None

        self.movable_group = pygame.sprite.Group()
        self.rooms = self.init_rooms()


    def init_rooms(self):
        room1 = Room(
            player_start=(9,4),
            map_path = "maps/room3.tmx",
            movable_group = self.movable_group,
            exits={}
        )

        self.current_room = room1

    def draw(self,surface):
        self.current_room.draw(surface)


    def recalc_layout(self):
        self.current_room.recalc_layout()

        new_tile_size = self.current_room.TILE_SIZE
        x_offset = self.current_room.x_offset
        y_offset = self.current_room.y_offset
        screen_w, screen_h = self.current_room.surface_width, self.current_room.surface_height
