import random
import pygame
from config import *
from game.platform import Platform
from game.coin import Coin


class Level:
    """
    Level - encapulates platforms and coins for a single level.

    Usage:
      level = Level()
      level.create_default_level()  # creates platforms
      level.spawn_coins(n=3)       # spawn N coins at random positions on platforms
    """

    def __init__(self):
        self.platforms = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()

    def create_default_level(self):
        # Create a few platforms at different heights and positions
        ground = Platform(0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40)
        middle = Platform(150, SCREEN_HEIGHT - 220, 220, 20)
        floating = Platform(500, SCREEN_HEIGHT - 320, 150, 20)
        small = Platform(350, SCREEN_HEIGHT - 120, 120, 20)

        for p in (ground, middle, floating, small):
            self.platforms.add(p)

    def randomize_platform_positions(self, min_y=100, max_y=None, player_x=100):
        """Randomize X and Y positions of non-ground platforms.

        Keeps platforms fully inside the screen. Ground (full-width) is left untouched.
        """
        if max_y is None:
            max_y = SCREEN_HEIGHT - 80

        for p in list(self.platforms):
            # skip ground-like platforms that span full width
            if p.rect.width >= SCREEN_WIDTH:
                continue

            # choose new x so platform stays on screen
            max_x = SCREEN_WIDTH - p.rect.width
            new_x = random.randint(0, max_x)

            # choose new y within bounds (min_y .. max_y - platform height)
            max_allowed_y = max_y - p.rect.height
            new_y = random.randint(min_y, max_allowed_y)

            p.rect.x = new_x
            p.rect.y = new_y

        # Ensure at least one platform is reachable by the player's jump
        # Compute maximum jump height from ground: v^2 / (2*g)
        try:
            max_jump = int((JUMP_POWER ** 2) / (2 * GRAVITY))
        except Exception:
            max_jump = 120

        # find ground top
        ground_top = None
        for p in self.platforms:
            if p.rect.width >= SCREEN_WIDTH:
                ground_top = p.rect.top
                break

        if ground_top is None:
            ground_top = SCREEN_HEIGHT - 40

        # desired platform vertical range: between (ground_top - max_jump + margin) and (ground_top - min_clear)
        margin = 10
        min_clear = 60
        desired_min = max(min_y, ground_top - max_jump + margin)
        desired_max = max(min_y, ground_top - min_clear)

        # pick a candidate non-ground platform and ensure it's within desired vertical range and horizontally near player_x
        non_ground = [p for p in self.platforms if p.rect.width < SCREEN_WIDTH]
        if non_ground:
            # check if any already within range
            ok = any(desired_min <= p.rect.top <= desired_max for p in non_ground)
            if not ok:
                p = random.choice(non_ground)
                # horizontal position near player_x
                half_w = p.rect.width // 2
                new_x = max(0, min(SCREEN_WIDTH - p.rect.width, int(player_x - half_w + random.randint(-80, 80))))
                # vertical position in desired range
                if desired_min >= desired_max:
                    new_y = desired_max
                else:
                    new_y = random.randint(desired_min, desired_max)

                p.rect.x = new_x
                p.rect.y = new_y

    def spawn_coins(self, n=3, radius=12, image_name=None):
        """Spawn n coins at random positions on the top surface of non-ground platforms.

        Coins will be centered above the platform (y = platform.top - radius - 4).
        """
        self.coins.empty()

        # choose candidate platforms (exclude full-width ground if desired)
        candidates = [p for p in self.platforms if p.rect.width < SCREEN_WIDTH]
        if not candidates:
            candidates = list(self.platforms)

        for _ in range(n):
            plat = random.choice(candidates)
            # x range inside the platform, leave margins
            left = plat.rect.left + radius + 4
            right = plat.rect.right - radius - 4
            if left >= right:
                x = plat.rect.centerx
            else:
                x = random.randint(left, right)

            y = plat.rect.top - radius - 4
            coin = Coin(x, y, radius=radius, image_name=image_name)
            self.coins.add(coin)

        return self.coins

    def draw(self, screen):
        for p in self.platforms:
            p.draw(screen)
        for c in self.coins:
            c.draw(screen)
