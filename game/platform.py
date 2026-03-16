import pygame
from config import *


class Platform(pygame.sprite.Sprite):
    """Platform sprite - statická plocha, na které může hráč stát."""

    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(PLATFORM_COLOR)
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, surface):
        surface.blit(self.image, self.rect)
