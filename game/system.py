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
    child = None  # the orbiting object


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
        mercury = Planet()
        self.add_orbiting_object(sol, mercury, .46 * AU, 87)

        #Venus
        venus = Planet()
        self.add_orbiting_object(sol, venus, .7 * AU, 224)

        #Earth
        earth = Planet()
        self.add_orbiting_object(sol, earth, 1 * AU, 365)

        #Mars
        mars = Planet()
        self.add_orbiting_object(sol, mars, 1.6 * AU, 686)

        #Jupiter
        jupiter = Planet()
        self.add_orbiting_object(sol, jupiter, 5.2 * AU, 4332)

        #Saturn
        saturn = Planet()
        self.add_orbiting_object(sol, saturn, 10 * AU, 10759)

        #Uranus
        uranus = Planet()
        self.add_orbiting_object(sol, uranus, 19 * AU, 30799)

        #Neptune
        neptune = Planet()
        self.add_orbiting_object(sol, neptune, 30 * AU, 60190)

    def add_orbiting_object(self, parent, child, distance, period, start_angle=None):
        '''helper function to add an object to the map with an orbit'''
        orbit = Orbit()
        orbit.parent = parent
        orbit.child = child
        orbit.period = period

        if start_angle is None:
            start_angle = random.randint(0, 359)

        start_angle = math.radians(start_angle)

        x = math.sin(start_angle) * distance
        y = math.cos(start_angle) * distance

        self.orbits.append(orbit)
        self.map.add_object(child, (x, y))


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
