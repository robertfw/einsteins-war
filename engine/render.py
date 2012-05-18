import pygame


class Sprite(pygame.sprite.Sprite):
    def update(self):
        self.rect = self.image.get_rect()


class Display(object):
    window = None

    def __init__(self, *args, **kwargs):
        self.window = pygame.display.set_mode(*args, **kwargs)

    def reset_view(self):
        self.window.fill((0, 0, 0))

    def update(self):
        pygame.display.update()

    def draw_sprite_map(self, sprites):
        for pos in sprites:
            sprite = sprites[pos]
            sprite.update()
            if sprite.image is not None and sprite.rect is not None:
                sprite.rect.center = pos
                self.window.blit(sprite.image, sprite.rect)
