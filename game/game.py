import pygame
from config import *

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.Clock = pygame.time.Clock()

    def handle_events(self):
        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def update(self):
        pass

    def draw(self):
        self.screen.fill(SKY_BLUE)
        pygame.display.flip()

    def run(self):
        self.running = True
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.Clock.tick(FPS)