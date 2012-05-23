from engine.map import Map2D, Map2DWindow
from engine.render import Sprite
from pygame import draw
from pygame.surface import Surface


class DumbMass(object):
    '''
    Represents a lump of collectable mass (asteroids, ship wrecks, etc)
    '''

    mass = None
    orbit = None


class Planet(object):
    '''
    Represents a planet
    '''

    age = None
    mass = None
    orbit = None

    def get_sprite(self):
        sprite = Sprite()
        surface = Surface((25, 25))
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

    # if the star is orbiting a barycenter (for example in a binary system etc), it has an orbit
    orbit = None

    def get_sprite(self):
        sprite = Sprite()
        surface = Surface((50, 50))
        draw.circle(surface, (255, 0, 0), (25, 25), 25, 0)
        sprite.image = surface

        return sprite


class Orbit(object):
    '''
    Represents an orbit
    '''

    period = None  # number of days to complete one orbit
    parent_object = None  # object the orbit is centered on


class System(object):
    '''
    Represents a single system
    '''

    map = None

    def __init__(self):
        self.map = Map2D()
        self.spawn_objects()

    def spawn_objects(self):
        star = Star()
        self.map.add_object(star, (0, 0))

        planet = Planet()
        
        #1 AU out
        self.map.add_object(planet, (149598000000, 149598000000))


class SystemWindow(Map2DWindow):
    '''Extends Map2DWindow to display a system'''
    system = None

    def __init__(self, *args, **kwargs):
        self.system = kwargs.get('system')
        kwargs['map2d'] = self.system.map
        super(SystemWindow, self).__init__(*args, **kwargs)

    def get_sprite_map(self, interpolation):
        objects = self.get_objects()
        sprites = {}
        for pos in objects:
            obj = objects[pos]
            if callable(obj.get_sprite):
                sprites[pos] = obj.get_sprite()
        
        return sprites
