from __future__ import division
from engine.map import Map2D, Map2DWindow
from engine.render import Sprite
from pygame import draw
from pygame.surface import Surface
import math
from engine.utils import memoize


@memoize
def generate_sphere_sprite(radius, color, scale):
    sprite = Sprite()
    surface = Surface((radius * 2, radius * 2))
    surface.set_colorkey((0, 0, 0))
    draw.circle(surface, color, (radius, radius), radius, 0)
    sprite.image = surface

    return sprite


class Barycenter(object):
    pass


class MassiveSpheroid(object):

    def get_sprite(self, scale):
        return generate_sphere_sprite(self.radius, self.color, scale)


class Moon(MassiveSpheroid):
    mass = None
    radius = 5
    color = (50, 50, 50)


class Planet(MassiveSpheroid):
    mass = None
    radius = 10
    color = (50, 200, 50)


class Star(MassiveSpheroid):
    mass = None
    radius = 25
    color = (255, 255, 50)


class Orbit(object):
    '''
    Represents an orbit
    '''

    period = None  # number of days to complete one orbit
    parent = None  # object the orbit is centered on
    radius = None  # radius of the orbit
    child = None  # the orbiting object
    _cur_angle = None  # radius of the orbit in degrees
    _angular_velocity = None  # how many degrees to move per tick

    def __init__(self, parent, child, period, radius, angle):
        self.parent = parent
        self.child = child
        self.period = period
        self.radius = radius
        self._cur_angle = angle

        self.child.orbit = self

        # determine our angular velocity, in degrees per second
        #self._angular_velocity = 360 / (self.period * 24 * 60 * 60)
        
        #temp debug override. reality is sooooooo slooooooooow
        self._angular_velocity = 360 / (self.period)

    def update_position(self, dt):
        self._cur_angle += self._angular_velocity * dt

        if self._cur_angle > 360:
            self._cur_angle -= 360

        #my math teacher always said i'd need this some day
        x = math.sin(self._cur_angle) * self.radius
        y = math.cos(self._cur_angle) * self.radius

        center = self.parent.get_position()

        position = (x + center[0], y + center[1])

        return position


class Galaxy(object):
    '''
    Represents a galaxy
    '''

    map = None
    orbits = []

    def __init__(self):
        self.map = Map2D()

    def update(self, dt):
        for orbit in self.orbits:
            position = orbit.update_position(dt)
            self.map.move_object(orbit.child, position)
