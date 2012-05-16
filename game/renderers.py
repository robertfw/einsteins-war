from game.system import Star
from pygame.sprite import Sprite
from pygame import draw
from pygame.surface import Surface


def render_system(renderer, system):
    objects = system.get_objects()
    sprites = []
    for pos in objects:
        obj = objects[pos]
        if obj is Star:
            sprites[pos] = generate_star_sprite(obj)


def generate_star_sprite(star):
    sprite = Sprite()
    surface = Surface((25, 25))
    draw.circle(surface, (255, 0, 0), (0, 0), 25, 0)
    sprite.image = surface

    return sprite
