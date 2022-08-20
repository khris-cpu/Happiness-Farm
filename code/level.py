from ipaddress import collapse_addresses
from re import T
import pygame
from settings import *
from player import Player
from overlay import Overlay
from sprites import Generic , Water , WildFlower , Tree
from pytmx.util_pygame import load_pygame
from support import *

class Level:
    def __init__(self):

        # get the display surface
        self.display_surface = pygame.display.get_surface() ## == self.screen
        # sprite group
        self.all_sprites = CameraGroup()
        self.collision_sprites = pygame.sprite.Group()

        self.setup()
        self.overlay = Overlay(self.player)

    def setup(self):
        
        ## Load map.tmx --> Tiled
        tmx_data = load_pygame('./data/map.tmx') 

        ## Load Elements

        ## house
        for layer in ['HouseFloor','HouseFurnitureBottom']:
            for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
                Generic((x * TILE_SIZE, y * TILE_SIZE),surf,self.all_sprites,LAYERS['house bottom'])
        
        for layer in ['HouseWalls','HouseFurnitureTop']:
            for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
                Generic((x * TILE_SIZE, y * TILE_SIZE),surf,self.all_sprites) ## Don;t have layers --> LAYERS['main'] == Default layer in Generic Class
        
        ## Fence
        for x, y, surf in tmx_data.get_layer_by_name('Fence').tiles():
                Generic((x * TILE_SIZE, y * TILE_SIZE),surf,[self.all_sprites,self.collision_sprites])

        ## Water
        water_frames = import_folder('./graphics/water')
        for x, y, surf in tmx_data.get_layer_by_name('Water').tiles():
                Water((x * TILE_SIZE, y * TILE_SIZE),water_frames,self.all_sprites)

        ## Wildflowers
        for obj in tmx_data.get_layer_by_name('Decoration'):
            WildFlower((obj.x,obj.y), obj.image , self.all_sprites)

        ## Trees
        for obj in tmx_data.get_layer_by_name('Trees'):
            Tree((obj.x,obj.y),obj.image,[self.all_sprites,self.collision_sprites],obj.name)

        ## Collsion Tiled
        for x,y,surf in tmx_data.get_layer_by_name('Collision').tiles():
            Generic((x * TILE_SIZE,y * TILE_SIZE), pygame.Surface((TILE_SIZE,TILE_SIZE)),self.collision_sprites)

        Generic(
            pos = (0,0),
            surf = pygame.image.load('./graphics/world/ground.png').convert_alpha(),
            groups = self.all_sprites,
            z = LAYERS['ground'] ## Layer of ground
        )

        ## Player Class
        for obj in tmx_data.get_layer_by_name('Player'):
            if obj.name == 'Start':
                self.player = Player((obj.x,obj.y),self.all_sprites,self.collision_sprites)

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
            ##For Player Behind the element --> sorted(self.sprites() , key = lambda sprite : sprite.rect.centery)
            for sprite in sorted(self.sprites() , key = lambda sprite : sprite.rect.centery):
                if layer == sprite.z:
                    offset_rect = sprite.rect.copy()  ## copy() --> return a same list
                    offset_rect.center -= self.offset ## Position of Player 
                    self.display_surface.blit(sprite.image,offset_rect)
