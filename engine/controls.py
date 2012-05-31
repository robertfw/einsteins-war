import pygame
from pygame.locals import KEYDOWN, KEYUP


class KeyBoardController(object):
    bindings = None

    def __init__(self, bindings=None):
        self.bindings = bindings

    def set_repeat(self, delay, interval):
        pygame.key.set_repeat(delay, interval)

    def handle(self, event):
        if event.type == KEYDOWN and event.key in self.bindings and 'down' in self.bindings[event.key]:
            self.bindings[event.key]['down']()
        elif event.type == KEYUP and event.key in self.bindings and 'up' in self.bindings[event.key]:
            self.bindings[event.key]['up']()
        
    def evaluate_keystates(self):
        keystates = pygame.key.get_pressed()
        for key in self.bindings:
            if keystates[key]:
                self.bindings[key]()
