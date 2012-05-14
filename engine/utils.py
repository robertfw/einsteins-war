import pygame
import sys
from pprint import pprint


def quit():
    pygame.quit()
    sys.exit()


def debug(msg):
    pprint(msg)
