import pygame
from settings import *
from player import Player
from overlay import Overlay
from sprites import Generic

class Level:
    def __init__(self):
        # get the display surface
        self.display_surface = pygame.display.get_surface() ## == self.screen
        # sprite group
        self.all_sprites = CameraGroup()
        self.setup()
        self.overlay = Overlay(self.player)

    def setup(self):
        Generic(
            pos = (0,0),
            surf = pygame.image.load('./Graphics Folder/Graphic Folder 3/world/ground.png').convert_alpha(),
            groups = self.all_sprites,
            z = LAYERS['ground'] ## Layer of ground
        )
        ## Player Class
        self.player = Player((640,320),self.all_sprites)

    def run(self,dt):
        self.display_surface.fill('black')
        self.all_sprites.customize_draw(self.player)
        self.all_sprites.update(dt)

        self.overlay.display()

## Camera Class Group
class CameraGroup(pygame.sprite.Group): ## --> All Background Item Group
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()

    def customize_draw(self,player):

        ## Shif the Background To Follow The Player
        self.offset.x = player.rect.centerx - SCREEN_WIDTH / 2
        self.offset.y = player.rect.centery - SCREEN_HEIGHT / 2

        for layer in LAYERS.values():
            for sprite in self.sprites():
                if layer == sprite.z:
                    offset_rect = sprite.rect.copy()  ## copy() --> return a same list
                    offset_rect.center -= self.offset ## Position of Player 
                    self.display_surface.blit(sprite.image,offset_rect)
