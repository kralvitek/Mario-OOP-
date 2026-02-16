from config import *

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        image_loaded = False

        for name in ["Cat_Mario", "cat", "player", "kocka"]:
            for ext in ["png", "jpg", "jpeg", "webp"]:
                try:
                    image_path = os.path.join("img", f"{name}.{ext}")
                    self.image = pygame.image.load(image_path).convert_alpha()
                    self.image = pygame.transform.scale(
                        self.image, (PLAYER_WIDTH, PLAYER_HEIGHT)
                    )
                    print(f"Načten obrázek: {image_path}")
                    image_loaded = True

                    break
                except (pygame.error, FileNotFoundError):
                    continue
            if image_loaded:
                
                self.image = pygame[PLAYER_HEIGHT, PLAYER_WIDTH]

                self.image.fill((255, 0, 0))  # Červená barva pro testování
                self.rect = self.image.get_rect()
                self.rect.topleft = (x, y)
                
                self.velocity_y = 0
                self.velocity_x = 0
                self.on_ground = False
                
            def update(self, platforms):
                self.velocity_y += 0.5  # Gravitace
                self.rect.y += self.velocity_y
                self.rect.x += self.velocity_x
                
                # Kontrola kolize s platformami
                for platform in platforms:
                    if self.rect.colliderect(platform.rect):
                        if self.velocity_y > 0:  # Pád dolů
                            self.rect.bottom = platform.rect.top
                            self.on_ground = True
                            self.velocity_y = 0
                        elif self.velocity_y < 0:  # Skok nahoru
                            self.rect.top = platform.rect.bottom
                            self.velocity_y = 0
                        if self.velocity_x > 0:  # Pohyb doprava
                            self.rect.right = platform.rect.left
                            self.velocity_x = 0
                        elif self.velocity_x < 0:  # Pohyb doleva
                            self.rect.left = platform.rect.right
                            self.velocity_x = 0