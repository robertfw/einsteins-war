import pygame
from pygame.locals import MOUSEBUTTONDOWN


class KeyBoardController(object):
    def __init__(self, bindings=None):
        self.bindings = bindings

    def set_repeat(self, delay, interval):
        pygame.key.set_repeat(delay, interval)

    def handle(self, event):
        try:
            callback = self.bindings[event.key][event.type]
            callback()
        except KeyError:
            pass


class MouseController(object):
    def __init__(self, bindings=None):
        self.bindings = bindings

    def handle(self, event):
        if event.type in self.bindings:
            if event.type == MOUSEBUTTONDOWN:
                if event.button in self.bindings[MOUSEBUTTONDOWN]:
                    self.bindings[MOUSEBUTTONDOWN][event.button](event)
            else:
                self.bindings[event.type](event)
