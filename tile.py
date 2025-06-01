import pygame


class Tile(pygame.sprite.Sprite):
    def __init__(self,pos, image, collidable =False ):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=pos)
        self.collidable = collidable
