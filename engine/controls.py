import pygame


class KeyBoardController(object):
    bindings = None

    def __init__(self, bindings=None):
        self.bindings = bindings

    def set_repeat(self, delay, interval):
        pygame.key.set_repeat(delay, interval)

    def evaluate_keystates(self):
        keystates = pygame.key.get_pressed()
        for key in self.bindings:
            if keystates[key]:
                self.bindings[key]()
