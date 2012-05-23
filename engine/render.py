import pygame
from pygame.rect import Rect


class Sprite(pygame.sprite.Sprite):
    
    def update(self):
        self.rect = self.image.get_rect()

    def set_rect_pos(self, pos):
        '''Proxy to self.rect position. sub classes can override this'''
        self.rect.center = pos


class Window(object):
    sprites = {}
    rect = None
    visible = True

    def __init__(self, *args, **kwargs):
        self.rect = Rect(kwargs.get('rect'))


class WindowManager(object):
    windows = []

    def add_window(self, window):
        self.windows.append(window)

    def get_window_layers(self, interpolation):
        window_layers = []

        generator = (window.get_sprite_map(interpolation=interpolation) for window in self.windows if window.visible)
        map(lambda layer: window_layers.append(layer), generator)

        return window_layers


class Display(object):
    window = None
    resolution = None

    def __init__(self, *args, **kwargs):
        self.window = pygame.display.set_mode(*args, **kwargs)
        
        info = pygame.display.Info()
        self.resolution = (info.current_w, info.current_h)

    def reset_view(self):
        self.window.fill((0, 0, 0))

    def update(self):
        pygame.display.update()

    def draw_sprite_map(self, layers):
        #TODO: not wild about this
        if type(layers).__name__ != 'list':
            layers = [layers]
        
        for sprites in layers:
            for pos in sprites:
                sprite = sprites[pos]
                sprite.update()
                if sprite.image is not None and sprite.rect is not None:
                    sprite.set_rect_pos(pos)
                    self.window.blit(sprite.image, sprite.rect)
