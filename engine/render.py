import pygame
import os.path


class Sprite(pygame.sprite.Sprite):
    base_image = None
    image = None
    rect = None

    def set_base_image_file(self, filepath):
        #TODO: should do some error checking here for bad paths
        self.set_base_image(pygame.image.load(os.path.join('assets', filepath)).convert_alpha())

    def set_base_image(self, image):
        self.base_image = image

    def update(self):
        self.update_image()
        self.update_rect()

    def update_image(self):
        self.image = self.base_image

    def update_rect(self):
        self.rect = self.image.get_rect()

    def set_rect_pos(self, pos):
        self.rect.center = pos


class Renderer(object):
    window = None
    fps_clock = None
    viewport_size = (0, 0)

    def __init__(self, viewport_size):
        self.viewport_size = viewport_size
        self.window = pygame.display.set_mode(self.viewport_size)

    def reset_view(self):
        self.window.fill((0, 0, 0))

    def update(self):
        pygame.display.update()

    def draw_sprite_map(self, sprites):
        for pos in sprites:
            sprite = sprites[pos]
            sprite.update()
            if sprite.image is not None and sprite.rect is not None:
                sprite.set_rect_pos(pos)
                self.window.blit(sprite.image, sprite.rect)
