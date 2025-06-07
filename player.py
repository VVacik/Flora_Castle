import pygame
from Settings import *
from grid_object import Grid_Object
from assets import *

direction_map = {0: "front", 1: "back", 2: "left", 3: "right"}
directions = {1: (0, -1), 0: (0, 1), 2: (-1, 0), 3: (1, 0)}

class Player(Grid_Object):
    def __init__(self,grid_position, tile_size, image, is_blocked = None, collidable = True, movable_objects_group = None, current_room = None):
        super().__init__(grid_position, tile_size, image, is_blocked, collidable)

        #Obiekty na planszy które gracz może złapać
        self.movable_objects_group = movable_objects_group
        self.held_object = None

        #Parametry dodatkowe:
        self.facing = 0
        self.energy = 100
        self.current_room = current_room
        self.set_current_room(current_room)


        self.static_images = {
            "front": PLAYER_IMG_FRONT,
            "back": PLAYER_IMG_BACK,
            "left": PLAYER_IMG_LEFT,
            "right": PLAYER_IMG_RIGHT,
        }

        self.animation_frames = {
            "front": [PLAYER_IMG_FRONT_A1, PLAYER_IMG_FRONT_A2],
            "back": [PLAYER_IMG_BACK_A1, PLAYER_IMG_BACK_A2],
            "left": [PLAYER_IMG_LEFT_A],
            "right": [PLAYER_IMG_RIGHT_A]
        }



        self.current_frame = 0
        self.animation_speed = 6
        self.animation_counter = 0
        self.images = self.static_images

    def set_current_room(self, current_room):
        self.current_room = current_room

    def update(self, dt):

        super().update(dt)
        self.update_animation()

    def update_sprite_direction(self):
        direction = direction_map.get(self.facing)

        if self.animating:

            frames = self.animation_frames[direction]
            self.original_image = frames[self.current_frame % len(frames)]
        else:

            self.original_image = self.static_images[direction]

        self.resize(self.tile_size)

    def resize(self, new_tile_size):
        self.tile_size = new_tile_size
        self.image = pygame.transform.scale(self.original_image, (self.tile_size, self.tile_size))
        self.rect = self.image.get_rect(topleft=(self.x, self.y))




    def update_animation(self):

        if self.animating:
            self.animation_counter += 1
            if self.animation_counter >= self.animation_speed:
                self.animation_counter = 0
                self.current_frame += 1
                self.update_sprite_direction()
        else:
            # Reset animacji gdy gracz przestaje się ruszać
            self.current_frame = 0
            self.animation_counter = 0
            self.update_sprite_direction()


    def handle_event(self, event):
        if event.type != pygame.KEYDOWN:
            return

        key_to_facing = {
            pygame.K_s: 0, pygame.K_DOWN: 0,
            pygame.K_w: 1, pygame.K_UP: 1,
            pygame.K_a: 2, pygame.K_LEFT: 2,
            pygame.K_d: 3, pygame.K_RIGHT: 3,
        }

        if event.key in key_to_facing:

            self.facing = key_to_facing[event.key]
            self.update_sprite_direction()
            if not self.animating:
                dx, dy = directions[self.facing]
                self.move(dx, dy)

    def can_move_to_position(self, new_grid_x, new_grid_y):

        if not (0 <= new_grid_x < self.screen_w and 0 <= new_grid_y < self.screen_h):
            return False


        temp_screen_x = self.current_room.x_offset + new_grid_x * self.current_room.TILE_SIZE
        temp_screen_y = self.current_room.y_offset + new_grid_y * self.current_room.TILE_SIZE
        temp_rect = pygame.Rect(temp_screen_x, temp_screen_y, self.current_room.TILE_SIZE, self.current_room.TILE_SIZE)


        if self.current_room.check_collision(temp_rect):
            print(f"Kolizja! Nie można iść na pozycje ({new_grid_x}, {new_grid_y})")
            return False
        return True

    def check_door_interaction(self):

            # Stwórz prostokąt na aktualnej pozycji gracza
        current_screen_x = self.current_room.x_offset + self.grid_x * self.current_room.TILE_SIZE
        current_screen_y = self.current_room.y_offset + self.grid_y * self.current_room.TILE_SIZE
        player_rect = pygame.Rect(current_screen_x, current_screen_y, self.current_room.TILE_SIZE,self.current_room.TILE_SIZE)

        # Sprawdź kolizję z drzwiami
        if self.current_room.check_door_collision(player_rect):
            door_position = self.current_room.get_colliding_door_position(player_rect)
            print(f"Gracz wszedł na drzwi na pozycji: {door_position}")

            return door_position

        return None

    def move(self, dx, dy):
        if self.animating:
            return

        new_player_x = self.grid_x + dx
        new_player_y = self.grid_y + dy

        if self.can_move_to_position(new_player_x, new_player_y):
            # Zapisz docelową pozycję
            self.target_grid_x = new_player_x
            self.target_grid_y = new_player_y

            self.animated_move(dx, dy)
            self.check_door_interaction()


