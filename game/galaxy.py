from __future__ import division
import math
from engine.map import Map2D
from engine.render import Sprite
from engine.utils import memoize
from pygame import draw
from pygame.surface import Surface


class GalaxyFactory(object):
    systems = []

    def register(self, func):
        self.systems.append(func)
        return func

    def create(self):
        galaxy = Galaxy()
        for system_generator in self.systems:
            system_generator(galaxy)

        return galaxy
        

@memoize
def generate_sphere_sprite(radius, color, scale, layer=None):
    scaled_radius = int(round(radius * scale))
    if scaled_radius <= 0:
        scaled_radius = 1
    
    sprite = Sprite()
    if layer is not None:
        sprite.layer = layer
    
    width = height = scaled_radius * 2
    surface = Surface((width, height))
    surface.set_colorkey((0, 0, 0))
    draw.circle(surface, color, (scaled_radius, scaled_radius), scaled_radius, 0)
    sprite.image = surface

    return sprite


class Barycenter(object):
    pass


class MassiveSpheroid(object):
    def __init__(self, mass=None, radius=600000000, color=(50, 50, 50)):
        self.mass = mass
        self.radius = radius
        self.color = color

    def get_sprite(self, scale):
        return generate_sphere_sprite(self.radius, self.color, scale, self.layer)


class Moon(MassiveSpheroid):
    layer = 0


class Planet(MassiveSpheroid):
    layer = 1


class Star(MassiveSpheroid):
    layer = 2


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
        self._angular_velocity = 360 / (self.period * 24 * 60 * 60)
        
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
