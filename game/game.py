import pygame
from config import *
from game.player import Player
from game.platform import Platform
from game.coin import Coin
from game.level import Level


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        self.playing = True
        self.game_over = False
        self.win = False

        # sprite groups
        self.all_sprites = pygame.sprite.Group()

        # player
        self.player = Player(100, 100)
        self.all_sprites.add(self.player)

        # level (platforms + coins)
        self.level = Level()
        self.level.create_default_level()
        self.level.randomize_platform_positions(player_x=self.player.rect.centerx)
        self.level.spawn_coins(n=COIN_COUNT, radius=COIN_RADIUS, image_name=COIN_IMAGE)

        for p in self.level.platforms:
            self.all_sprites.add(p)
        for c in self.level.coins:
            self.all_sprites.add(c)

        try:
            self.font = pygame.font.Font(None, 48)
        except Exception:
            self.font = None

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and self.game_over:
                    self.reset_level()
                if event.key in (pygame.K_q, pygame.K_ESCAPE):
                    self.running = False

    def update(self):
        # update player
        game_over = self.player.update(self.level.platforms)
        if game_over:
            self.playing = False
            self.game_over = True
            self.win = False

        # collisions with coins
        hit_coins = pygame.sprite.spritecollide(self.player, self.level.coins, dokill=True)
        if hit_coins:
            for c in hit_coins:
                if c in self.all_sprites:
                    self.all_sprites.remove(c)

        # win condition
        if len(self.level.coins) == 0:
            self.playing = False
            self.game_over = True
            self.win = True

    def draw(self):
        self.screen.fill(SKY_BLUE)
        for sprite in self.all_sprites:
            sprite.draw(self.screen)

        if self.game_over:
            self.draw_game_over()

        pygame.display.flip()

    def run(self):
        self.running = True
        while self.running:
            self.handle_events()
            if self.playing:
                self.update()
            self.draw()
            self.clock.tick(FPS)

    def reset_level(self):
        # remove existing coins from all_sprites
        for c in list(self.level.coins):
            if c in self.all_sprites:
                self.all_sprites.remove(c)

        # randomize platforms and respawn coins
        self.level.randomize_platform_positions(player_x=self.player.rect.centerx)
        self.level.spawn_coins(n=COIN_COUNT, radius=COIN_RADIUS, image_name=COIN_IMAGE)

        for c in self.level.coins:
            self.all_sprites.add(c)

        # reset player
        self.player.rect.x = 100
        self.player.rect.y = 100
        self.player.velocity_x = 0
        self.player.velocity_y = 0
        self.player.on_ground = False

        # reset flags
        self.playing = True
        self.game_over = False
        self.win = False

    def draw_game_over(self):
        if not self.font:
            return

        if self.win:
            text = "You win! Press R to play again or Q to quit"
        else:
            text = "Game Over! Press R to restart or Q to quit"

        surf = self.font.render(text, True, (255, 255, 255))
        rect = surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 120))
        self.screen.blit(overlay, (0, 0))
        self.screen.blit(surf, rect)