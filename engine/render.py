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
    display = None

    def __init__(self, display):
        self.display = display

    def add_window(self, window):
        self.windows.append(window)

    def render(self, interpolation):
        offset_layers = []

        for window in self.windows:
            if window.visible:
                layers = window.get_sprite_map(interpolation=interpolation)

                if type(layers).__name__ != 'list':
                    layers = [layers]

                for layer in layers:
                    offset_layer = {}
                    # we need to offset the position of the sprites based on the window position
                    for pos in layer:
                        new_pos = (pos[0] + window.rect.centerx, pos[1] + window.rect.centery)
                        offset_layer[new_pos] = layer[pos]

                    offset_layers.append(offset_layer)
        
        self.display.draw_sprite_map(offset_layers)

    def get_sprite_map(self):
        '''abstract, should return a map of sprites, keyed by position'''
        pass


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
