from assets import *
import pygame
from room import Room
from player import Player


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

        self.player = Player(
            grid_position=room1.player_start,
            tile_size= room1.TILE_SIZE,
            movable_objects_group= room1.movable_group,
            image=PLAYER_IMG_FRONT,
            is_blocked =self.is_blocked,
            current_room=room1

        )


        self.player_group = pygame.sprite.GroupSingle(self.player)
        self.player.resize(room1.TILE_SIZE)
        self.player.set_offset(room1.x_offset, room1.y_offset)

        self.current_room = room1

    def draw(self,surface):
        self.current_room.draw(surface)
        self.player_group.draw(surface)

    def is_blocked(self,x,y):
        return

    def update(self,dt):
        self.player_group.update(dt)
        self.current_room.update(dt)


    def recalc_layout(self):
        self.current_room.recalc_layout()

        new_tile_size = self.current_room.TILE_SIZE
        x_offset = self.current_room.x_offset
        y_offset = self.current_room.y_offset
        screen_w, screen_h = self.current_room.surface_width, self.current_room.surface_height

        self.player.set_offset(x_offset, y_offset)
        self.player.resize(new_tile_size)
        self.player.update_pixel_position()

