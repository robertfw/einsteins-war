import pygame
import sys
from pprint import pprint


def memoize(func):
    cache = {}

    def memoized(*args):
        if args not in cache:
            cache[args] = func(*args)
            
        return cache[args]

    return memoized
    

def quit():
    pygame.quit()
    sys.exit()


def debug(msg):
    pprint(msg)
