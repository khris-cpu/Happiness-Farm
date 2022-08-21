from re import X
import pygame
from settings import *
from random import randint,choice
from timer import Timer

## General Sprites
class Generic(pygame.sprite.Sprite):
    def __init__(self,pos,surf,groups,z = LAYERS['main']):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        self.z = z
        self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.2,-self.rect.height * 0.75)

class Water(Generic):
    def __init__(self, pos, frames, groups):
        
        ## Animation set up
        self.frames = frames
        self.frames_index = 0

        ## Sprites setup
        super().__init__(
            pos = pos , 
            surf = self.frames[self.frames_index],
            groups = groups,
            z = LAYERS['water'])

    def animated(self,dt):
        self.frames_index += 4 * dt
        if self.frames_index >= len(self.frames):
            self.frames_index = 0
        self.image = self.frames[int(self.frames_index)]

    def update(self,dt):
        self.animated(dt)

class WildFlower(Generic):
    def __init__(self, pos, surf, groups):
        super().__init__(pos, surf, groups)
        self.hitbox = self.rect.copy().inflate(-20,self.rect.height * 0.9)

class Tree(Generic):
    def __init__(self, pos, surf, groups,name): ## name --> Small , Large
        super().__init__(pos, surf, groups)

        ## Tree attributes
        self.health = 5
        self.alive = True
        stump_path = f'./graphics/stumps/{"small" if name == "Small" else "large"}.png'
        self.stump_surf = pygame.image.load(stump_path) ## Tree Destroy
        self.invul_timer = Timer(200)

        ## apples
        self.apples_surf = pygame.image.load("./graphics/fruit/apple.png")
        self.apples_pos = APPLE_POS[name]
        self.apple_sprites = pygame.sprite.Group()
        self.create_fruit()

    def damage(self):
        
        ## Damaging the tree
        self.health =- 1
        ## remove apple
        if len(self.apple_sprites.sprites()) > 0:
            random_apple = choice(self.apple_sprites.sprites())
            random_apple.kill()

    def check_death(self):
        if self.health <= 0:
            self.image = self.stump_surf
            self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
            self.hitbox = self.rect.copy().inflate((-10,-self.rect.height * 0.6))
            self.alive = False

    def update(self,dt):
        if self.alive == True:
            self.check_death()

    def create_fruit(self):
        for pos in self.apples_pos:
            if randint(0,10) < 2:
                x = pos[0] + self.rect.left ## Left Side
                y = pos[1] + self.rect.top ## Top Side
                Generic(
                    pos = (x,y),
                    surf = self.apples_surf,
                    groups = [self.apple_sprites,self.groups()[0]],
                    z = LAYERS['fruit'])
