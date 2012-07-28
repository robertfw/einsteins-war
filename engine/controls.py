import pygame
from pygame.locals import KEYDOWN, KEYUP, MOUSEBUTTONDOWN


class KeyBoardController(object):
    def __init__(self, bindings=None):
        self.bindings = bindings

    def set_repeat(self, delay, interval):
        pygame.key.set_repeat(delay, interval)

    def handle(self, event):
        if event.type == KEYDOWN and event.key in self.bindings and 'down' in self.bindings[event.key]:
            self.bindings[event.key]['down']()
        elif event.type == KEYUP and event.key in self.bindings and 'up' in self.bindings[event.key]:
            self.bindings[event.key]['up']()


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
