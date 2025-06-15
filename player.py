import pygame
from Settings import *
from grid_object import Grid_Object
from assets import *

direction_map = {0: "front", 1: "back", 2: "left", 3: "right"}
directions = {1: (0, -1), 0: (0, 1), 2: (-1, 0), 3: (1, 0)}


doors = {
    "up" : ((7,1), (8,1)),
    "right": ((12,4), (12, 5)),
    "down": ((7, 8), (8,8)),
    "left": ((3, 4), (3,5)),
}

class Player(Grid_Object):
    def __init__(self, grid_position, image,tile_size, is_blocked=None, collidable=True, movable_objects_group=None,
                 current_room=None):
        # Przesunięcia: X ma być na środku
        # Y przesunięty o 1/3 kafelka
        render_offset_x = 0
        render_offset_y = -tile_size // 3



        super().__init__(grid_position,  image, tile_size, is_blocked, collidable, (render_offset_x, render_offset_y))

        # Obiekty na planszy które gracz może złapać
        self.movable_objects_group = movable_objects_group
        self.held_object = None

        # Parametry dodatkowe:
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
        old_tile_size = self.tile_size
        self.tile_size = new_tile_size

        # Przeskaluj obrazek
        self.image = pygame.transform.scale(self.original_image, (self.tile_size, self.tile_size))

        # Przeskaluj render offset proporcjonalnie
        if old_tile_size > 0:
            scale_factor = new_tile_size / old_tile_size
            self.render_offset_x *= scale_factor
            self.render_offset_y *= scale_factor

        # Zaktualizuj rozmiar collision rect
        self.collision_rect.size = (self.tile_size, self.tile_size)

    def update_animation(self):
        # Jeśli animacja trwa, Sprawdzaj czy ilość tików w animacji jest większa niż prędkość


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


        elif event.key == pygame.K_e and not self.held_object and self.movable_objects_group:
            self.pick_up(self.movable_objects_group)

        elif event.key == pygame.K_r and self.held_object:
            self.throw()

    def can_move_to_position(self, new_grid_x, new_grid_y, ignore=None):
        if not (0 <= new_grid_x < self.screen_w and 0 <= new_grid_y < self.screen_h):
            return False

        # Sprawdzenie czy Nowa pozycja Kafelka zawiera element kolizyjny
        temp_screen_x = self.current_room.x_offset + new_grid_x * self.current_room.TILE_SIZE
        temp_screen_y = self.current_room.y_offset + new_grid_y * self.current_room.TILE_SIZE
        temp_rect = pygame.Rect(temp_screen_x, temp_screen_y, self.current_room.TILE_SIZE, self.current_room.TILE_SIZE)

        if self.current_room.check_collision(temp_rect):
            print(f"Kolizja! Nie można iść na pozycje ({new_grid_x}, {new_grid_y})")
            return False

        # Sprawdź kolizję z ruchomymi obiektami (jeśli grupa istnieje)
        if self.movable_objects_group:
            for obj in self.movable_objects_group:
                # Pomiń obiekt który ma być ignorowany
                if obj is ignore:
                    continue
                # Sprawdź czy obiekt zajmuje docelową pozycję
                if obj.grid_x == new_grid_x and obj.grid_y == new_grid_y:
                    return False

        return True

    def check_door_interaction(self):
        # Sprawdzenie funkcją kolizyjną czy gracz wchodzi w interakcje z drzwiami
        current_screen_x = self.current_room.x_offset + self.grid_x * self.current_room.TILE_SIZE
        current_screen_y = self.current_room.y_offset + self.grid_y * self.current_room.TILE_SIZE
        player_collision_rect = pygame.Rect(current_screen_x, current_screen_y, self.current_room.TILE_SIZE, self.current_room.TILE_SIZE)

        # Sprawdź kolizję z drzwiami
        if self.current_room.check_door_collision(player_collision_rect):
            door_position = self.current_room.get_colliding_door_position(player_collision_rect)
            print(f"Gracz wszedł na drzwi na pozycji: {door_position}")
            return door_position

        return None

    def move(self, dx, dy):

        if self.check_door_interaction() is not None:
            self.animating = False

        if self.animating:
            return

        new_player_x = self.grid_x + dx
        new_player_y = self.grid_y + dy

        if self.held_object:
            new_obj_x = self.held_object.grid_x + dx
            new_obj_y = self.held_object.grid_y + dy


            obj_can_move = self.can_move_to_position(new_obj_x, new_obj_y, ignore=self.held_object)
            player_can_move = (self.can_move_to_position(new_player_x, new_player_y, ignore=self.held_object) or
                               (self.held_object.grid_x == new_player_x and self.held_object.grid_y == new_player_y))

            Have_energy = (self.energy > 0)

            if obj_can_move and player_can_move and Have_energy:
                self.held_object.animated_move(dx, dy)
                self.animated_move(dx, dy)
                self.energy -= 5





        else:
            if self.can_move_to_position(new_player_x, new_player_y):
                self.animated_move(dx, dy)





    def pick_up(self, objects_group):

        direction = directions[self.facing]
        target_x = self.grid_x + direction[0]
        target_y = self.grid_y + direction[1]


        for obj in objects_group:
            if obj.grid_x == target_x and obj.grid_y == target_y:
                self.held_object = obj
                self.held_object.original_image = ROCK_FLOATING.convert_alpha()
                self.held_object.resize(self.tile_size)
                self.held_object.animation_duration = 0.25

                break

    def throw(self):

        if self.energy > 0:
            if not self.held_object:
                return

            self.held_object.animation_duration = 0.1

            direction = directions[self.facing]
            obj = self.held_object
            obj_x, obj_y = obj.grid_x, obj.grid_y
            path = []

            while True:
                next_x = obj_x + direction[0]
                next_y = obj_y + direction[1]

                current_screen_x = self.current_room.x_offset + next_x * self.current_room.TILE_SIZE
                current_screen_y = self.current_room.y_offset + next_y * self.current_room.TILE_SIZE
                obj_rect = pygame.Rect(current_screen_x, current_screen_y, self.tile_size, self.tile_size)

                if not self.can_move_to_position(next_x, next_y) or ( next_x == self.grid_x and next_y == self.grid_y) or self.current_room.check_door_collision(obj_rect):
                    break

                obj_x, obj_y = next_x, next_y
                path.append((obj_x, obj_y))

            if path:
                obj.throw_path = path
                obj.throwing = True
                obj.throw_timer = 0

        self.held_object.original_image = ROCK_IMG.convert_alpha()
        self.held_object.resize(self.tile_size)
        self.held_object = None








