import pygame
from settings import *
from player import Player

class Level:
    def __init__(self):
        # get the display surface
        self.display_surface = pygame.display.get_surface() ## == self.screen
        # sprite group
        self.all_sprites = pygame.sprite.Group() ## Draw and update Sprites --> Tree,Plants
        self.setup()

    def setup(self):
        ## Player Class
        self.player = Player((640,320),self.all_sprites)

    def run(self,dt):
        self.display_surface.fill('black')
        self.all_sprites.draw(self.display_surface)
        self.all_sprites.update(dt)
