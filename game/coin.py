import os
import pygame
from config import *


class Coin(pygame.sprite.Sprite):
    """Simple coin sprite.

    Notes:
    - Attempts to load an image from img/ when created. If image is missing,
      falls back to drawing a filled circle.
    - The coin manages its own surface and rect for collisions.
    """

    def __init__(self, x, y, radius=12, image_name=None):
        super().__init__()
        self.radius = radius

        # visual representation of the coin by dropping an image into the img/
        # folder (the image is scaled to radius*2). If the image is missing or
        # fails to load we fall back to a simple drawn circle.
        try:
            image_path = os.path.join("img", image_name)
            img_surface = pygame.image.load(image_path).convert_alpha()
            img_surface = pygame.transform.scale(img_surface, (radius * 2, radius * 2))
            self.image = img_surface
        except Exception:
            # image load failed -> use fallback drawable
            self.image = self._make_circle_surface(radius)

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def _make_circle_surface(self, radius):
        diameter = radius * 2
        surf = pygame.Surface((diameter, diameter), pygame.SRCALPHA)
        pygame.draw.circle(surf, (255, 215, 0), (radius, radius), radius)
        return surf

    def draw(self, screen):
        screen.blit(self.image, self.rect)
