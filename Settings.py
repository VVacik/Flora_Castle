def calculate_tile_size(screen_width, screen_height):


    tile_width = (screen_width - (GRID_WIDTH - 1) * TILE_SPACING) // GRID_WIDTH
    tile_height = (screen_height - (GRID_HEIGHT +60) * TILE_SPACING) // GRID_HEIGHT

    return min(tile_width, tile_height)

GRID_WIDTH = 8
GRID_HEIGHT = 6

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
TILE_SPACING = 3

FPS = 60
PLAYER_START_ENERGY = 100

COLOR_BG = (30, 30, 30)
COLOR_GRID = (50, 50, 50)
