from settings import *

class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surf = pygame.display.get_surface()

    def draw(self):
        for sprite in self:
            for i in range(5):
                self.display_surf.blit(sprite.shadow_surf, sprite.rect.topleft + pygame.Vector2(i, i))

        for sprite in self:
            self.display_surf.blit(sprite.image, sprite.rect)
