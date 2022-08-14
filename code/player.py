import pygame
from settings import *
from support import *
from timer import Timer

class Player(pygame.sprite.Sprite): ## pygame.spriteSprite --> Simple base class for visible game objects.
    def __init__ (self, pos , group):
        super().__init__(group)

        self.import_assets()
        self.status = 'down' ## Image --> Player Activity

        ## Frame Index --> a Number of Picture => 0,1,2,3...
        self.frame_index = 0  ## In Image Folder Start at 0

        ## general setup
        self.image = self.animations[self.status][self.frame_index]  ## Call The Animations
        self.rect = self.image.get_rect(center = pos) ## Position

        ## movement attributes
        self.direction = pygame.math.Vector2() ## 2-Dimensional Vector
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 200

        ## timers
        self.timers = {
            'tool use' : Timer(350,self.use_tool) ## Set the time of Tools animation 
        }

        ## tools
        self.selected_tool = 'hoe'

    def use_tool(self):
        print(self.selected_tool)

    def import_assets(self):

        ## Animations
        self.animations = {'up': [],'down' : [] , 'left' : [] , 'right' : [] , ## Player Animation Movement
                            'right_idle' : [] , 'left_idle' : [] , 'up_idle' : [] , 'down_idle' : [], ## Idle Animation Movement
                            'right_hoe' : [] , 'left_hoe' : [] , 'up_hoe' : [] , 'down_hoe' : [], ## hoe Animation Movement
                            'right_axe' : [] , 'left_axe' : [] , 'up_axe' : [] , 'down_axe' : [], ## Axe Animation Movement
                            'right_water' : [] , 'left_water' : [] , 'up_water' : [] , 'down_water' : []} ## Water Animation Movement

        for animation in self.animations.keys() :
            full_path = './Graphics Folder/Graphic Folder 1/character/' + animation ## Import All Animations of Character in Graphics Folder
            self.animations[animation] = import_folder(full_path) ## Call import_folder function

    def animate(self,dt):
        self.frame_index += 4 * dt
        if self.frame_index >= len(self.animations[self.status]):  ## In Our Folder in limits Only 4 Pictures
            self.frame_index = 0

        self.image = self.animations[self.status][int(self.frame_index)]

    def input(self):

        keys = pygame.key.get_pressed()

        if not self.timers['tool use'].active:

            ## Direction
            if keys[pygame.K_w]: ## up
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_s]: ## down
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0

            if keys[pygame.K_d]: ## right
                self.direction.x = 1
                self.status = 'right'
            elif keys[pygame.K_a]: ## left
                self.direction.x = -1
                self.status = 'left'
            else :
                self.direction.x = 0

            ## tool use
            if keys[pygame.K_SPACE]:
                self.timers['tool use'].activate()
                self.direction = pygame.math.Vector2()
                self.frame_index = 0

    def get_status(self):
        
        ## movement
        if self.direction.magnitude() == 0:
            self.status = self.status.split('_')[0] + '_idle'
        
        ## tool use
        if self.timers['tool use'].active:
            self.status = self.status.split('_')[0] + '_' + self.selected_tool

    def update_timers(self):
        for timer in self.timers.values():
                timer.update()

    def move(self,dt):

        ## normalizing vector
        if self.direction.magnitude() > 0: ## Euclidean --> Euclic
            self.direction = self.direction.normalize() ##  vector with the same direction but length 1.
        
        ## horizontal movement (Left & Right)
        self.pos.x += self.direction.x * self.speed * dt
        self.rect.centerx = self.pos.x
        ## vertical movement (Up & Down)
        self.pos.y += self.direction.y * self.speed * dt
        self.rect.centery = self.pos.y
    
    def update(self,dt):

        ## Call Function
        self.input()
        self.get_status()
        self.update_timers()
        self.move(dt)
        self.animate(dt) 
