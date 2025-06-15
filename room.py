import pygame
import pytmx
from pytmx.util_pygame import load_pygame
from tile import Tile
from assets import *



class Room:
    def __init__(self, player_start, map_path, movable_group,exits, additional_col = None):
        #parametry pobrane z konstruktora
        self.player_start = player_start
        self.map_path = map_path
        self.movable_group = movable_group
        self.additional_col = additional_col
        self.exits = exits

        # Trzymamy tu wymiary ekranu, Rozmiar kafelka, oraz przesunięcia ekranu

        self.screen = pygame.display.get_surface()
        self.surface_width, self.surface_height = self.screen.get_size()
        self.TILE_SIZE = 0
        self.x_offset = 0
        self.y_offset = 0

        #Pobieramy dane z pliku tmx i ustawiamy wymiary mapy w kafelkach
        self.tmx_data = load_pygame(self.map_path)
        self.map_width= self.tmx_data.width
        self.map_height = self.tmx_data.height

        # Nowe listy dla warstw kolizji i drzwi
        self.collision_tiles = []
        self.door_tiles = []

        #Grupa na Kafelki oraz array na (X kafelka, y kafelka, obrazek)
        self.tile_group = pygame.sprite.Group()
        self.tiles_info = []

        #Wywoływane metody przy tworzeniu pokoju:
        self.load_tiles_from_map()
        self.recalc_layout()



    def load_tiles_from_map(self):
            for layer in self.tmx_data.layers:
                if isinstance(layer, pytmx.TiledTileLayer):
                    layer_name = layer.name.lower()

                    for x, y, gid in layer:
                        if gid is not None:
                            if layer_name == "collison":
                                if not gid ==0:
                                    self.collision_tiles.append((x, y))
                            elif layer_name == "doors":
                                if not gid == 0:
                                    self.door_tiles.append((x, y))
                            else:
                                tile_img = self.tmx_data.get_tile_image_by_gid(gid)
                                if tile_img is not None:
                                    self.tiles_info.append((x, y, tile_img))



    def create_collision_hitboxes(self):



        for x, y in self.collision_tiles:
            screen_x = self.x_offset + x * self.TILE_SIZE
            screen_y = self.y_offset + y * self.TILE_SIZE

            collision_rect = pygame.Rect(screen_x, screen_y, self.TILE_SIZE, self.TILE_SIZE)


        for x, y in self.door_tiles:
            screen_x = self.x_offset + x * self.TILE_SIZE
            screen_y = self.y_offset + y * self.TILE_SIZE

            door_rect = pygame.Rect(screen_x, screen_y, self.TILE_SIZE, self.TILE_SIZE)
        if self.movable_group is not None:
            for object in self.movable_group.sprites():
                screen_x = self.x_offset + object.rect.x * self.TILE_SIZE
                screen_y = self.y_offset + object.rect.y * self.TILE_SIZE

                collision_rect = pygame.Rect(screen_x, screen_y, self.TILE_SIZE, self.TILE_SIZE)

        if self.additional_col is not None:
            for object in self.additional_col.sprites():
                screen_x = self.x_offset + object.rect.x * self.TILE_SIZE
                screen_y = self.y_offset + object.rect.y * self.TILE_SIZE

                collision_rect = pygame.Rect(screen_x, screen_y, self.TILE_SIZE, self.TILE_SIZE)



    #Metoda Przeliczająca rozmiary spritów w zależności od rozmiaru ekranu
    def recalc_layout(self):
        self.surface_width, self.surface_height = self.screen.get_size()

        self.TILE_SIZE = min(
            self.surface_width / self.map_width,
            self.surface_height / self.map_height
        )

        map_pixel_width = self.TILE_SIZE * self.map_width
        map_pixel_height = self.TILE_SIZE * self.map_height

        self.x_offset = (self.surface_width - map_pixel_width) / 2
        self.y_offset = (self.surface_height - map_pixel_height) / 2

        self.tile_group.empty()

        for x_tile, y_tile, original_image in self.tiles_info:
            scaled_img = pygame.transform.scale(original_image, (self.TILE_SIZE, self.TILE_SIZE))
            screen_x = self.x_offset + x_tile * self.TILE_SIZE
            screen_y = self.y_offset + y_tile * self.TILE_SIZE

            tile = Tile((screen_x, screen_y), scaled_img)
            self.tile_group.add(tile)

        self.create_collision_hitboxes()



    def get_collision_rects(self):
        """Zwraca listę prostokątów kolizji"""
        collision_rects = []
        for x, y in self.collision_tiles:
            screen_x = self.x_offset + x * self.TILE_SIZE
            screen_y = self.y_offset + y * self.TILE_SIZE
            collision_rects.append(pygame.Rect(screen_x, screen_y, self.TILE_SIZE, self.TILE_SIZE))

        if self.movable_group is not None:
            for x in self.movable_group.sprites():
                collision_rects.append(pygame.Rect(x.rect.x, x.rect.y, self.TILE_SIZE, self.TILE_SIZE))

        if self.additional_col is not None:
            for object in self.additional_col.sprites():
                collision_rects.append(pygame.Rect(object.rect.x, object.rect.y, self.TILE_SIZE, self.TILE_SIZE))

        return collision_rects

    def get_door_rects(self):
        """Zwraca listę prostokątów drzwi"""
        door_rects = []
        for x, y in self.door_tiles:
            screen_x = self.x_offset + x * self.TILE_SIZE
            screen_y = self.y_offset + y * self.TILE_SIZE
            door_rects.append(pygame.Rect(screen_x, screen_y, self.TILE_SIZE, self.TILE_SIZE))
        return door_rects

    def check_collision(self, rect):
        """Sprawdza kolizję z warstwą kolizji"""
        collision_rects = self.get_collision_rects()
        for collision_rect in collision_rects:
            if rect.colliderect(collision_rect):
                return True
        return False

    def check_door_collision(self, rect):
        """Sprawdza kolizję z drzwiami"""
        door_rects = self.get_door_rects()
        for door_rect in door_rects:
            if rect.colliderect(door_rect):
                return True
        return False

    def get_colliding_door_position(self, rect):
        """Zwraca pozycję drzwi z którymi koliduje rect"""
        door_rects = self.get_door_rects()
        for i, door_rect in enumerate(door_rects):
            if rect.colliderect(door_rect):
                return self.door_tiles[i]
        return None

    def update(self, dt):
        return

    def draw_debug_hitboxes(self, surface):

        # Rysuj drzwi na niebiesko
        for rect in self.get_door_rects():
            pygame.draw.rect(surface, (0, 0, 255, 100), rect, 2)
        # Rysuj kolizje na czerwono
        for rect in self.get_collision_rects():
            pygame.draw.rect(surface, (255, 0, 0, 100), rect, 2)

    def has_exit(self, direction):
        """Sprawdź czy pokój ma wyjście w danym kierunku"""
        return direction in self.exits and self.exits[direction] is not None

    def get_exit_room(self, direction):
        """Pobierz ID pokoju do którego prowadzi ten kierunek"""
        return self.exits.get(direction)

    def draw(self, surface):
        self.tile_group.draw(surface)

        #self.draw_debug_hitboxes(surface)







