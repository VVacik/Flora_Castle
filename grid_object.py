import pygame

class Grid_Object(pygame.sprite.Sprite):
    def __init__(self, grid_position, tile_size, image, is_blocked=None, collidable = True):
        super().__init__()
        #Pola pobrane z konstruktora
        self.grid_x, self.grid_y = grid_position
        self.tile_size = tile_size
        self.original_image = image
        self.image = pygame.transform.scale(self.original_image, (self.tile_size, self.tile_size))
        self.collidable = collidable
        self.is_blocked = is_blocked

        #offsety ekranu i inicjalizacja hitboxa
        self.x_offset = 0
        self.y_offset = 0
        self.rect = self.image.get_rect()

        #Pobierane znowu!!!!
        self.screen_w, self.screen_h = pygame.display.get_surface().get_size()

        #Parametry do animowania:
        self.animating = False
        self.animation_start_pos = (0,0)
        self.animation_end_pos = (0,0)
        self.animation_duration = 0.1
        self.animation_time_elapsed = 0.0

        #Pozycja w pikselach:
        self.x, self.y = 0, 0

        #Wywoływane metody:
        self.set_offset(self.x_offset, self.y_offset)

    def update_pixel_position(self):
        self.x = self.grid_x * self.tile_size + self.x_offset
        self.y = self.grid_y * self.tile_size + self.y_offset
        self.rect.topleft = (round(self.x), round(self.y))

    def set_offset(self, x_offset, y_offset):
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.update_pixel_position()

    def resize(self, new_tile_size):
        self.tile_size = new_tile_size
        self.original_image = pygame.transform.scale(self.original_image, (self.tile_size, self.tile_size))
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.update_pixel_position()

