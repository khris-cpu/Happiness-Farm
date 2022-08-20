from os import supports_fd
import pygame
from settings import *

class Generic(pygame.sprite.Sprite):
    def __init__(self,pos,surf,groups,z = LAYERS['main']):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        self.z = z

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

class Tree(Generic):
    def __init__(self, pos, surf, groups,name):
        super().__init__(pos, surf, groups,name)