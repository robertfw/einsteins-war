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
        full_sprite_map = {}
        for window in self.windows:
            if window.visible:
                sprite_map = window.get_sprite_map(interpolation=interpolation)

                # we need to offset the position of the sprites based on the window position
                for pos in sprite_map:
                    new_pos = (pos[0] + window.rect.centerx, pos[1] + window.rect.centery)
                    full_sprite_map[new_pos] = sprite_map[pos]
        
        self.display.draw_sprite_map(full_sprite_map)

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

    def draw_sprite_map(self, sprites):
        for pos in sprites:
            sprite = sprites[pos]
            sprite.update()
            if sprite.image is not None and sprite.rect is not None:
                sprite.set_rect_pos(pos)
                self.window.blit(sprite.image, sprite.rect)
