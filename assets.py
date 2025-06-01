import os
import pygame

ASSET_DIR = "assets"

def load_image(filename, size=None):
    path = os.path.join(ASSET_DIR, filename)
    image = pygame.image.load(path)
    if size is not None:
        image = pygame.transform.scale(image, size)
    return image



BACKGROUND_IMG = load_image("background.png")
PLAYER_IMG_FRONT = load_image("front_idle.png")
PLAYER_IMG_BACK = load_image("back_idle.png")
PLAYER_IMG_LEFT = load_image("left_idle.png")
PLAYER_IMG_RIGHT = load_image("right_idle.png")
TILE_IMG = load_image("Tile.png")
ROCK_IMG = load_image("rock.png")