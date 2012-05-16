from __future__ import division
from engine.map import Map2D, Map2DWindow
from engine.render import Sprite
from pygame import draw
from pygame.surface import Surface
import random
import math


class DumbMass(object):
    '''
    Represents a lump of collectable mass (asteroids, ship wrecks, etc)
    '''

    mass = None


class Planet(object):
    '''
    Represents a planet
    '''

    mass = None

    def get_sprite(self):
        sprite = Sprite()
        surface = Surface((25, 25))
        surface.set_colorkey((0, 0, 0))
        draw.circle(surface, (0, 255, 0), (12, 12), 12, 0)
        sprite.image = surface

        return sprite


class Star(object):
    '''
    Represents a star (or black hole)
    '''

    # most characteristics of stars can be derived from their initial mass and their current age
    # age is in millions of years, initial_mass is in solar masses
    age = None
    initial_mass = None

    def get_sprite(self):
        sprite = Sprite()
        surface = Surface((50, 50))
        surface.set_colorkey((0, 0, 0))
        draw.circle(surface, (255, 0, 0), (25, 25), 25, 0)
        sprite.image = surface

        return sprite


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

        # determine our angular velocity, in degrees per second
        self._angular_velocity = 360 / (self.period * 24 * 60 * 60)
        self._angular_velocity = 360 / (self.period)

        #temporary override so this stuff is visible instead of real time
        #self._angular_velocity = 1

    def update_position(self, dt):
        self._cur_angle += self._angular_velocity * dt

        if self._cur_angle > 360:
            self._cur_angle -= 360

        x = math.sin(self._cur_angle) * self.radius
        y = math.cos(self._cur_angle) * self.radius

        return (x, y)


class System(object):
    '''
    Represents a single system
    '''

    map = None
    orbits = []

    def __init__(self):
        self.map = Map2D()
        self.spawn_objects()

    def spawn_objects(self):
        #TODO: put this in a more accessible place
        AU = 149598000000  # 1 AU in meters

        AU = 100

        #TODO: these should not be here
        sol = Star()
        self.map.add_object(sol, (0, 0))

        #Mercury
        self.mercury = Planet()
        self.add_orbiting_object(sol, self.mercury, .46 * AU, 87)

        #Venus
        self.venus = Planet()
        self.add_orbiting_object(sol, self.venus, .7 * AU, 224)

        #Earth
        self.earth = Planet()
        self.add_orbiting_object(sol, self.earth, 1 * AU, 365)

        #Mars
        self.mars = Planet()
        self.add_orbiting_object(sol, self.mars, 1.6 * AU, 686)

        #Jupiter
        self.jupiter = Planet()
        self.add_orbiting_object(sol, self.jupiter, 5.2 * AU, 4332)

        #Saturn
        self.saturn = Planet()
        self.add_orbiting_object(sol, self.saturn, 10 * AU, 10759)

        #Uranus
        self.uranus = Planet()
        self.add_orbiting_object(sol, self.uranus, 19 * AU, 30799)

        #Neptune
        self.neptune = Planet()
        self.add_orbiting_object(sol, self.neptune, 30 * AU, 60190)

    def add_orbiting_object(self, parent, child, distance, period, start_angle=None):
        '''helper function to add an object to the map with an orbit'''
        if start_angle is None:
            start_angle = random.randint(0, 359)

        start_angle = math.radians(start_angle)

        orbit = Orbit(parent=parent, child=child, period=period, angle=start_angle, radius=distance)

        position = orbit.update_position(0)

        self.orbits.append(orbit)
        return self.map.add_object(child, position)

    def update_orbits(self, dt):
        for orbit in self.orbits:
            position = orbit.update_position(dt)
            self.map.move_object(orbit.child, position)


class SystemWindow(Map2DWindow):
    '''Extends Map2DWindow to display a system'''
    system = None

    def __init__(self, *args, **kwargs):
        self.system = kwargs.get('system')
        kwargs['map2d'] = self.system.map
        super(SystemWindow, self).__init__(*args, **kwargs)

    def get_sprite_map(self, interpolation):
        objects = self.get_objects()
        
        layers = [{}, {}]
        for pos in objects:
            obj = objects[pos]
            
            if isinstance(obj, Star):
                layers[1][pos] = obj.get_sprite()
            elif isinstance(obj, Planet):
                layers[0][pos] = obj.get_sprite()
        
        return layers
