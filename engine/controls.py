import pygame


class KeyBoardController(object):
    bindings = None

    def __init__(self, bindings=None):
        self.bindings = bindings

    def set_repeat(self, delay, interval):
        pygame.key.set_repeat(delay, interval)

    def evaluate_keystates(self, keystates):
        #TODO: instead of evaluating all of our keystates, it would likely be faster
        # to just check the pressed keys for keybinds
        for key in self.bindings:
            if keystates[key]:
                self.bindings[key]()
