import pygame
from settings import *
from support import *
from timer import Timer

class Player(pygame.sprite.Sprite): ## pygame.spriteSprite --> Simple base class for visible game objects.
    def __init__ (self, pos , group, collision_sprites,tree_sprites,interaction,soil_layer,toggle_shop):
        super().__init__(group)

        self.import_assets()
        self.status = 'down' ## Image --> Player Activity

        ## Frame Index --> a Number of Picture => 0,1,2,3...
        self.frame_index = 0  ## In Image Folder Start at 0

        ## general setup
        self.image = self.animations[self.status][self.frame_index]  ## Call The Animations
        self.rect = self.image.get_rect(center = pos) ## X,Y Position
        self.z = LAYERS['main'] ## Player Layers --> Z position

        ## movement attributes
        self.direction = pygame.math.Vector2() ## 2-Dimensional Vector
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 200

        ## collisions
        self.collision_sprites=  collision_sprites
        self.hitbox = self.rect.copy().inflate((-126,-70))

        ## timers
        self.timers = {
            'tool use' : Timer(350,self.use_tool), ## Set the time of Tools animation 
            'tool switch' : Timer(200),
            'seed use' : Timer(350,self.use_seed),
            'seed switch' : Timer(200)
        }

        ## tools
        self.tools = ['hoe','axe','water']
        self.tool_index = 0
        self.selected_tool = self.tools[self.tool_index]

        ## seeds
        self.seeds = ['rice','tomato','cabbage','beatroot','cauliflower','cucumber',
                      'eggplant','flower','radish','carrot','pumkin','purple cauliflower']
        self.seed_index = 0
        self.selected_seed = self.seeds[self.seed_index]

        ## inventory
        self.item_inventory = {
            'wood' : 0,
            'apple' : 0,
            'rice' : 0,
            'tomato' : 0,
            'cabbage' : 0,
            'cauliflower' : 0,
            'cucumber' : 0,
            'eggplant' : 0,
            'carrot' : 0,
            'pumkin' : 0,
        }

        self.seed_inventory = {
            'rice' : 5,
            'tomato' : 5,
            'cabbage' : 5,
            'cauliflower' : 5,
            'cucumber' : 5,
            'eggplant' : 5,
            'carrot' : 5,
            'pumkin' : 5,
        }
        self.money = 200

        ## Interaction
        self.tree_sprites = tree_sprites
        self.interaction = interaction
        self.sleep = False
        self.soil_layer = soil_layer
        self.toggle_shop = toggle_shop

    def use_tool(self):
        if self.selected_tool == 'hoe':
            self.soil_layer.get_hit(self.target_pos)
        elif self.selected_tool == 'axe':
            for tree in self.tree_sprites.sprites():
                if tree.rect.collidepoint(self.target_pos):
                    tree.damage()
        elif self.selected_tool == 'water':
            self.soil_layer.water(self.target_pos)
    
    def get_target_pos(self):
        self.target_pos = self.rect.center + PLAYER_TOOL_OFFSET[self.status.split('_')[0]]

    def use_seed(self):
        if self.seed_inventory[self.selected_seed] > 0:
            self.seed_inventory[self.selected_seed] -= 1
        self.soil_layer.plant_seed(self.target_pos,self.selected_seed)

    def import_assets(self):

        ## Animations
        self.animations = {'up': [],'down' : [] , 'left' : [] , 'right' : [] , ## Player Animation Movement
                            'right_idle' : [] , 'left_idle' : [] , 'up_idle' : [] , 'down_idle' : [], ## Idle Animation Movement
                            'right_hoe' : [] , 'left_hoe' : [] , 'up_hoe' : [] , 'down_hoe' : [], ## hoe Animation Movement
                            'right_axe' : [] , 'left_axe' : [] , 'up_axe' : [] , 'down_axe' : [], ## Axe Animation Movement
                            'right_water' : [] , 'left_water' : [] , 'up_water' : [] , 'down_water' : []} ## Water Animation Movement

        for animation in self.animations.keys() :
            full_path = './graphics/character/' + animation ## Import All Animations of Character in Graphics Folder
            self.animations[animation] = import_folder(full_path) ## Call import_folder function

    ## Animations
    def animate(self,dt):
        self.frame_index += 13 * dt
        if self.frame_index >= len(self.animations[self.status]):  ## In Our Folder in limits Only 4 Pictures
            self.frame_index = 0

        self.image = self.animations[self.status][int(self.frame_index)]

    def input(self):

        keys = pygame.key.get_pressed()

        if not self.timers['tool use'].active and not self.sleep: ## If self.timers != False and Sleep

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

            ## Change Tool
            if keys[pygame.K_q] and not self.timers['tool switch'].active:
                self.timers['tool switch'].activate()
                self.tool_index += 1
                if self.tool_index >= len(self.tools):
                    self.tool_index = 0
                self.selected_tool = self.tools[self.tool_index]

            # seed use
            if keys[pygame.K_v]:
                self.timers['seed use'].activate()
                self.direction = pygame.math.Vector2()
                self.frame_index = 0

            ## change use 
            if keys[pygame.K_e] and not self.timers['seed switch'].active:
                self.timers['seed switch'].activate()
                self.seed_index += 1
                if self.seed_index >= len(self.seeds):
                    self.seed_index = 0
                self.selected_seed = self.seeds[self.seed_index]

            ## Use Bed
            if keys[pygame.K_f]:
                self.toggle_shop()
                collided_interaction_sprite = pygame.sprite.spritecollide(self,self.interaction,False)
                if collided_interaction_sprite:
                    if collided_interaction_sprite[0].name == 'Trader':
                        self.toggle_shop()
                    else:
                        self.status = 'left_idle'
                        self.sleep = True

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

    ## Collision Function
    def collision(self,direction):
        for sprite in self.collision_sprites.sprites():
            if hasattr(sprite,'hitbox'):
                if sprite.hitbox.colliderect(self.hitbox):
                    if direction == 'horizontal':
                        if self.direction.x > 0: ## move right
                            self.hitbox.right = sprite.hitbox.left
                        if self.direction.x < 0: ## move left
                            self.hitbox.left = sprite.hitbox.right
                        self.rect.centerx = self.hitbox.centerx
                        self.pos.x = self.hitbox.centerx
                        
                    if direction == 'vertical':
                        if self.direction.y > 0: ## move down
                            self.hitbox.bottom = sprite.hitbox.top
                        if self.direction.y < 0: ## move up
                            self.hitbox.top = sprite.hitbox.bottom
                        self.rect.centery = self.hitbox.centery
                        self.pos.y = self.hitbox.centery

    def move(self,dt):

        ## normalizing vector
        if self.direction.magnitude() > 0: ## Euclidean --> Euclic
            self.direction = self.direction.normalize() ##  vector with the same direction but length 1.
        
        ## horizontal movement (Left & Right)
        self.pos.x += self.direction.x * self.speed * dt
        self.hitbox.centerx = round(self.pos.x)
        self.rect.centerx = self.hitbox.centerx
        self.collision('horizontal') ## Call Collision

        ## vertical movement (Up & Down)
        self.pos.y += self.direction.y * self.speed * dt
        self.hitbox.centery = round(self.pos.y)
        self.rect.centery = self.hitbox.centery
        self.collision('vertical')
    
    def update(self,dt):

        ## Call Function
        self.input()
        self.get_status()
        self.update_timers()
        self.get_target_pos()
        self.move(dt)
        self.animate(dt) 
