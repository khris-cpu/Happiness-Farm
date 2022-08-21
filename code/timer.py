import pygame

## To get Slow Down The Animation
class Timer:
    def __init__(self,duration,func = None):
        self.duration = duration ## ระยะเวลา --> To Check Where is time already now
        self.func = func
        self.start_time = 0 ## Start Time
        self.active = False

    def activate(self):
        self.active = True
        self.start_time = pygame.time.get_ticks() ## get the time in milliseconds

    def deactivate(self):
        self.active = False
        self.start_time = 0

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time >= self.duration:
            if self.func and self.start_time != 0:
                self.func()
            self.deactivate()