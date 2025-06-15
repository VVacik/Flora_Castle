import pygame


class Grid_Object(pygame.sprite.Sprite):
    def __init__(self, grid_position, image, tile_size , is_blocked=None, collidable=True, render_offset=(0, 0)):
        super().__init__()
        # Pola pobrane z konstruktora
        self.grid_x, self.grid_y = grid_position
        self.tile_size = tile_size
        self.original_image = image.convert_alpha()
        self.image = pygame.transform.scale(self.original_image, (self.tile_size, self.tile_size))
        self.collidable = collidable
        self.is_blocked = is_blocked

        # Przesunięcie renderowania względem pozycji logicznej
        self.render_offset_x, self.render_offset_y = render_offset

        # offsety ekranu i inicjalizacja hitboxa
        self.x_offset = 0
        self.y_offset = 0

        # Rect do renderowania
        self.rect = self.image.get_rect()
        if self.render_offset_y == 0 and self.render_offset_x == 0:
            self.rect = pygame.Rect(0, 0, self.tile_size, self.tile_size)

        #Collision rect - używany do kolizji, zawsze wpisany w kafelek
        self.collision_rect = pygame.Rect(0, 0, self.tile_size, self.tile_size)

        # Pobieranie wymiarów okna
        self.screen_w, self.screen_h = pygame.display.get_surface().get_size()

        # Parametry do animowania:
        self.animating = False
        self.animation_start_pos = (0, 0)
        self.animation_end_pos = (0, 0)
        self.animation_duration = 0.25
        self.animation_time_elapsed = 0.0

        # Pozycja w pikselach:
        self.x, self.y = 0, 0

        # Wywoływane metody:
        self.set_offset(self.x_offset, self.y_offset)




    def update_pixel_position(self):
        # Pozycja logiczna (środek kafelka)
        self.x = self.grid_x * self.tile_size + self.x_offset
        self.y = self.grid_y * self.tile_size + self.y_offset

        # Hitbox wpisany w kafelek
        self.collision_rect.topleft = (round(self.x), round(self.y))

        # Rendering rect - z przesunięciem
        render_x = self.x + self.render_offset_x
        render_y = self.y + self.render_offset_y
        self.rect.topleft = (round(render_x), round(render_y))

    def set_offset(self, x_offset, y_offset):
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.update_pixel_position()

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

        self.update_pixel_position()

    def set_render_offset(self, offset_x, offset_y):
        """Ustawia przesunięcie renderowania względem pozycji logicznej"""
        self.render_offset_x = offset_x
        self.render_offset_y = offset_y
        self.update_pixel_position()

    def get_collision_rect(self):
        """Zwraca prostokąt używany do kolizji"""
        return self.collision_rect

    def animated_move(self, dx, dy):
        if self.animating:
            return

        new_x = self.grid_x + dx
        new_y = self.grid_y + dy

        self.animating = True
        self.animation_time_elapsed = 0.0

        # Pozycje animacji dla renderowania (z offsetem)
        self.animation_start_pos = (self.x + self.render_offset_x, self.y + self.render_offset_y)

        self.grid_x, self.grid_y = new_x, new_y

        end_x = self.grid_x * self.tile_size + self.x_offset + self.render_offset_x
        end_y = self.grid_y * self.tile_size + self.y_offset + self.render_offset_y
        self.animation_end_pos = (end_x, end_y)

    def update(self, dt):
        if self.animating:
            self.animation_time_elapsed += dt
            progress = min(self.animation_time_elapsed / self.animation_duration, 1.0)

            # Animuj pozycję renderowania
            start_x, start_y = self.animation_start_pos
            end_x, end_y = self.animation_end_pos
            render_x = start_x + (end_x - start_x) * progress
            render_y = start_y + (end_y - start_y) * progress

            self.rect.topleft = (render_x, render_y)

            # Zaktualizuj też collision rect (bez offsetu renderowania)
            collision_x = render_x - self.render_offset_x
            collision_y = render_y - self.render_offset_y
            self.collision_rect.topleft = (collision_x, collision_y)

            if progress >= 1.0:
                self.animating = False
                self.update_pixel_position()  # Ustaw finalne pozycje