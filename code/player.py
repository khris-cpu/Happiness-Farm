import pygame
from settings import *

class Player(pygame.sprite.Sprite): ## pygame.spriteSprite --> Simple base class for visible game objects.
    def __init__ (self, pos , group):
        super().__init__(group)

        ## general setup
        self.image = pygame.Surface((32,64))
        self.image.fill('green')
        self.rect = self.image.get_rect(center = pos) ## Position

        ## movement attributes
        self.direction = pygame.math.Vector2() ## 2-Dimensional Vector
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 200

    def input(self):

        ## input key
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]: ## up
            self.direction.y = -1
        elif keys[pygame.K_s]: ## down
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_d]: ## right
            self.direction.x = 1
        elif keys[pygame.K_a]: ## left
            self.direction.x = -1
        else :
            self.direction.x = 0

    def move(self,dt):

        ## normalizing vector
        if (self.direction.magnitude() > 0): ## Euclidean --> Euclic
            self.direction = self.direction.normalize() ##  vector with the same direction but length 1.
            print(self.direction)
        
        ## horizontal movement (Left & Right)
        self.pos.x += self.direction.x * self.speed * dt
        self.rect.centerx = self.pos.x
        ## vertical movement (Up & Down)
        self.pos.y += self.direction.y * self.speed * dt
        self.rect.centery = self.pos.y
    

    def update(self,dt):
        self.input()
        self.move(dt)