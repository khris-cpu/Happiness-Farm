import pygame, sys
from settings import *
from level import Level
from pygame import mixer

class Game:
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.level = Level()
        pygame.display.set_caption('Happiness Farm')
        mixer.init()
        BG_MUSIC = mixer.music.load('./audio/001 - Stardew Valley Overture.mp3')
        mixer.music.set_volume(0.2)
        mixer.music.play(-1)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            dt = self.clock.tick(60)/1000
            self.level.run(dt)
            pygame.display.update()

if __name__ == '__main__':
    game = Game()
    game.run()
