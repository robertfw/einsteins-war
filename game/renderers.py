from game.system import Star
from engine.render import Sprite
from pygame import draw
from pygame.surface import Surface


def get_system_sprites(system):
    objects = system.get_objects()
    sprites = {}
    for pos in objects:
        obj = objects[pos]
        if isinstance(obj, Star):
            sprites[pos] = generate_star_sprite(obj)

    return sprites


def generate_star_sprite(star):
    sprite = Sprite()
    surface = Surface((50, 50))
    draw.circle(surface, (255, 0, 0), (25, 25), 25, 0)
    sprite.set_base_image(surface)

    return sprite
