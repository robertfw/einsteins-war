from engine.render import Sprite
from pygame.surface import Surface
from engine.utils import memoize
from pygame import draw


class RigidBody(object):
    mass = 10  # in kilograms
    vector = (0, 0)
    acceleration = (0, 0)

    def update_position(self, dt):
        self.vector = (self.vector[0] + self.acceleration[0] * dt, self.vector[1] + self.acceleration[1] * dt)
        cur_pos = self.get_position()
        new_pos = (cur_pos[0] + self.vector[0], cur_pos[1] + self.vector[1])

        self.map.move_object(self, new_pos)


class Ship(RigidBody):
    size = 10

    @memoize
    def get_sprite(self, scale):
        height = int(round(self.size * scale))
        width = height / 3
        if height <= 0:
            height = 3
            width = 1

        sprite = Sprite()
        sprite.layer = 10
        surface = Surface((width, height))
        surface.set_colorkey((0, 0, 0))

        points = [(width / 2, 0), (0, height), (width, height)]
        draw.polygon(surface, (255, 255, 255), points)

        sprite.image = surface

        return sprite
