# Enhanced LevelManager with room switching system

from assets import *
import pygame
from room import Room
from player import Player
from Movable_Object import Movable_Object

doors = {
    "up": ((7, 1), (8, 1)),
    "right": ((12, 4), (12, 5)),
    "down": ((7, 8), (8, 8)),
    "left": ((3, 4), (3, 5)),
}

# Mapowanie pozycji drzwi na kierunki
door_direction_map = {
    ((7, 1), (8, 1)): "up",
    ((12, 4), (12, 5)): "right",
    ((7, 8), (8, 8)): "down",
    ((3, 4), (3, 5)): "left",
}

# Przeciwne kierunki dla przejść między pokojami
opposite_direction = {
    "up": "down",
    "down": "up",
    "left": "right",
    "right": "left"
}


class LevelManager:
    def __init__(self):
        self.rooms = {}
        self.current_room_id = None
        self.current_room = None
        self.placeholder = 60
        self.movable_group = pygame.sprite.Group()

        # Najpierw inicjalizuj pokoje
        self.init_rooms()
        self.init_objects()
        self.recalc_layout()



    def init_rooms(self):
        # Definicja połączeń pokojów - każdy pokój wie, który pokój łączy się z każdym wyjściem
        room_connections = {
            "room1": {
                "up": "room2",
                "right": "room3",
                "down": "room4",
                "left": "room5"
            },
            "room2": {
                "up": None,
                "right": None,
                "down": "room1",
                "left": None,
            },
            "room3": {
                "up": None,
                "right": None,
                "down": None,
                "left": "room1"
            },

            "room4": {
                "up": "room1",
                "right": None,
                "down": None,
                "left": None
            },
            "room5": {
                "up": None,
                "right": "room1",
                "down": None,
                "left": None
            }


        }

        # Tworzenie pokojów
        self.rooms["room1"] = Room(
            player_start=(9, 4),
            map_path="maps/room1.tmx",
            movable_group=self.movable_group,
            exits=room_connections["room1"]
        )

        self.rooms["room2"] = Room(
            player_start=(7, 7),
            map_path="maps/room2.tmx",
            movable_group=None,
            exits=room_connections["room2"]
        )

        self.rooms["room3"] = Room(
            player_start=(11, 4),
            map_path="maps/room3.tmx",
            movable_group=None,
            exits=room_connections["room3"]
        )

        self.rooms["room4"] = Room(
            player_start=(11, 4),
            map_path="maps/room4.tmx",
            movable_group=None,
            exits=room_connections["room4"]
        )

        self.rooms["room5"] = Room(
            player_start=(11, 4),
            map_path="maps/room5.tmx",
            movable_group=None,
            exits=room_connections["room5"]
        )

        # Ustaw pokój startowy
        self.current_room_id = "room1"
        self.current_room = self.rooms[self.current_room_id]

        # Stwórz gracza
        self.player = Player(
            grid_position=self.current_room.player_start,
            tile_size=self.current_room.TILE_SIZE,
            movable_objects_group=self.current_room.movable_group,
            image=PLAYER_IMG_FRONT,
            is_blocked=self.is_blocked,
            current_room=self.current_room
        )

        self.player_group = pygame.sprite.GroupSingle(self.player)
        self.player.resize(self.current_room.TILE_SIZE)
        self.player.set_offset(self.current_room.x_offset, self.current_room.y_offset)

    def init_objects(self):
        # Dodaj obiekty tylko do room1 na początku
        rock1 = Movable_Object(
            grid_position=(4, 2),
            image=ROCK_IMG,
            tile_size=self.placeholder,
            collidable=True,
            is_blocked=self.is_blocked,
        )
        self.movable_group.add(rock1)

    def change_room(self):
        """Obsługuje przejścia między pokojami gdy gracz dotknie drzwi"""
        door_position = self.player.check_door_interaction()
        if door_position is None:
            return



        #Kierunek
        exit_direction = None
        for door_pos, direction in door_direction_map.items():
            if door_position in door_pos:
                exit_direction = direction
                break

        if exit_direction is None:
            print("Unknown door position!")
            return



        # Pobierz docelowy pokój z wyjść aktualnego pokoju
        target_room_id = self.current_room.exits.get(exit_direction)
        if target_room_id is None or target_room_id not in self.rooms:
            print(f"No room connected to {exit_direction} exit")
            return

        # Przełącz na nowy pokój
        old_room_id = self.current_room_id
        self.current_room_id = target_room_id
        self.current_room = self.rooms[target_room_id]

        # Umieść gracza przy odpowiednim wejściu w nowym pokoju
        entrance_direction = opposite_direction[exit_direction]
        new_player_position = self.get_entrance_position(entrance_direction)

        # Zaktualizuj referencję pokoju gracza i pozycję
        self.player.set_current_room(self.current_room)

        self.player.grid_x, self.player.grid_y = new_player_position
        self.player.movable_objects_group = self.current_room.movable_group

        # Przelicz layout dla nowego pokoju
        self.recalc_layout()



    def get_entrance_position(self, entrance_direction):
        """Pobierz pozycję spawnu gracza na podstawie kierunku wejścia"""
        door_positions = {
            "up": (self.player.grid_x , self.player.grid_y - 6),
            "down": (self.player.grid_x , self.player.grid_y + 6),
            "left": (self.player.grid_x - 8 , self.player.grid_y),
            "right": (self.player.grid_x +8 , self.player.grid_y )
        }

        return door_positions.get(entrance_direction, self.current_room.player_start)

    def draw(self, surface):
        self.current_room.draw(surface)
        if self.current_room.movable_group:
            self.current_room.movable_group.draw(surface)
        self.player_group.draw(surface)

    def is_blocked(self, x, y):
        return False

    def update(self, dt):

        self.player_group.update(dt)
        if self.player.check_door_interaction() is not None:
            self.change_room()
            self.player.animating = False
        self.current_room.update(dt)

        # Zaktualizuj ruchome obiekty w aktualnym pokoju
        if self.current_room.movable_group:
            for obj in self.current_room.movable_group:
                obj.set_offset(self.current_room.x_offset, self.current_room.y_offset)
            self.current_room.movable_group.update(dt)


    def recalc_layout(self):
        self.current_room.recalc_layout()

        new_tile_size = self.current_room.TILE_SIZE
        x_offset = self.current_room.x_offset
        y_offset = self.current_room.y_offset

        self.player.set_offset(x_offset, y_offset)
        self.player.resize(new_tile_size)
        self.player.update_pixel_position()

        # Zaktualizuj tylko obiekty w aktualnym pokoju
        if self.current_room.movable_group:
            for obj in self.current_room.movable_group.sprites():
                obj.resize(new_tile_size)
                obj.set_offset(x_offset, y_offset)