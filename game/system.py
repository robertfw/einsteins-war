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


class Moon(object):
    '''
    Represents a planet
    '''

    mass = None

    def get_sprite(self):
        sprite = Sprite()
        surface = Surface((10, 10))
        surface.set_colorkey((0, 0, 0))
        draw.circle(surface, (55, 55, 55), (5, 5), 5, 0)
        sprite.image = surface

        return sprite


class Planet(object):
    '''
    Represents a planet
    '''

    mass = None

    def get_sprite(self):
        sprite = Sprite()
        surface = Surface((20, 20))
        surface.set_colorkey((0, 0, 0))
        draw.circle(surface, (0, 255, 0), (10, 10), 10, 0)
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
        #self._angular_velocity = 360 / (self.period * 24 * 60 * 60)
        
        #temp debug override
        self._angular_velocity = 360 / (self.period)

    def update_position(self, dt, map2d):
        self._cur_angle += self._angular_velocity * dt

        if self._cur_angle > 360:
            self._cur_angle -= 360

        x = math.sin(self._cur_angle) * self.radius
        y = math.cos(self._cur_angle) * self.radius

        center = map2d.get_position(self.parent)

        position = (x + center[0], y + center[1])

        return position


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

        AU = 500  # override - full value is crashing big rects

        #TODO: solar system definition should be in a config file
        sol = Star()
        self.map.add_object(sol, (0, 0))

        #Mercury
        mercury = Planet()
        self.add_orbiting_object(sol, mercury, .46 * AU, 87)

        #Venus
        venus = Planet()
        self.add_orbiting_object(sol, venus, .7 * AU, 224)

        #Earth
        earth = Planet()
        self.add_orbiting_object(sol, earth, 1 * AU, 365)

        self.add_orbiting_object(earth, Moon(), .25 * AU, 29)

        #Mars
        mars = Planet()
        self.add_orbiting_object(sol, mars, 1.6 * AU, 686)

        self.add_orbiting_object(mars, Moon(), .25 * AU, 30)
        self.add_orbiting_object(mars, Moon(), .35 * AU, 65)

        #Jupiter
        jupiter = Planet()
        self.add_orbiting_object(sol, jupiter, 5.2 * AU, 4332)
        self.add_orbiting_object(jupiter, Moon(), .25 * AU, 30)
        self.add_orbiting_object(jupiter, Moon(), .35 * AU, 65)
        self.add_orbiting_object(jupiter, Moon(), .40 * AU, 95)
        self.add_orbiting_object(jupiter, Moon(), .50 * AU, 115)

        #Saturn
        saturn = Planet()
        self.add_orbiting_object(sol, saturn, 10 * AU, 10759)
        self.add_orbiting_object(saturn, Moon(), .25 * AU, 30)
        self.add_orbiting_object(saturn, Moon(), .35 * AU, 65)
        self.add_orbiting_object(saturn, Moon(), .40 * AU, 95)
        self.add_orbiting_object(saturn, Moon(), .50 * AU, 115)

        #Uranus
        uranus = Planet()
        self.add_orbiting_object(sol, uranus, 19 * AU, 30799)
        self.add_orbiting_object(uranus, Moon(), .25 * AU, 30)
        self.add_orbiting_object(uranus, Moon(), .35 * AU, 65)

        #Neptune
        neptune = Planet()
        self.add_orbiting_object(sol, neptune, 30 * AU, 60190)
        self.add_orbiting_object(neptune, Moon(), .25 * AU, 30)

    def add_orbiting_object(self, parent, child, distance, period, start_angle=None):

        '''helper function to add an object to the map with an orbit'''

        if start_angle is None:
            start_angle = random.randint(0, 359)

        start_angle = math.radians(start_angle)

        orbit = Orbit(parent=parent, child=child, period=period, angle=start_angle, radius=distance)

        position = orbit.update_position(0, self.map)

        self.orbits.append(orbit)
        return self.map.add_object(child, position)

    def update_orbits(self, dt):
        for orbit in self.orbits:
            position = orbit.update_position(dt, self.map)
            self.map.move_object(orbit.child, position)


class SystemWindow(Map2DWindow):
    '''Extends Map2DWindow to display a system'''
    system = None

    def __init__(self, *args, **kwargs):
        self.system = kwargs.get('system')
        kwargs['map2d'] = self.system.map
        super(SystemWindow, self).__init__(*args, **kwargs)

    def get_sprite_map(self, interpolation):
        if interpolation == 0:
            self.viewable_objects = self.get_objects()

        #TODO: implement orbit interpolation
        
        #TODO: this layering logic shouldn't be hardcoded
        layers = [{}, {}, {}]
        for pos in self.viewable_objects:
            obj = self.viewable_objects[pos]
                        
            if isinstance(obj, Star):
                layers[0][pos] = obj.get_sprite()
            elif isinstance(obj, Planet):
                layers[1][pos] = obj.get_sprite()
            elif isinstance(obj, Moon):
                layers[2][pos] = obj.get_sprite()
        
        return layers
