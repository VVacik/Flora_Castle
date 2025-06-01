import pygame
import pytmx
from pytmx.util_pygame import load_pygame
from tile import Tile
from assets import *


class Room:
    def __init__(self, player_start, map_path, movable_group, exits):
        #parametry pobrane z konstruktora
        self.player_start = player_start
        self.map_path = map_path
        self.movable_group = movable_group
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

        #Grupa na Kafelki oraz array na (X kafelka, y kafelka, obrazek)
        self.tile_group = pygame.sprite.Group()
        self.tiles_info = []

        #Wywoływane metody przy tworzeniu pokoju:
        self.load_tiles_from_map()
        self.recalc_layout()

    def load_tiles_from_map(self):
        for layer in self.tmx_data.layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile_img = self.tmx_data.get_tile_image_by_gid(gid)
                    if tile_img is not None:
                        self.tiles_info.append((x, y, tile_img))


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

    def update(self, dt):
        print("tu bedzie update")

    def draw(self, surface):
        self.tile_group.draw(surface)
        #






