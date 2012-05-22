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

    def get_objects(self):
        return self.map.objects

    def spawn_objects(self):
        self.map.add_object(Star(), (0, 0))
        self.map.add_object(Planet(), (100, 50))
        self.map.add_object(Planet(), (200, -20))
        self.map.add_object(Planet(), (-40, 100))
        self.map.add_object(Planet(), (-20, -80))

    def get_sprites(self):
        objects = self.get_objects()
        sprites = {}
        for pos in objects:
            obj = objects[pos]
            if callable(obj.get_sprite):
                sprites[pos] = obj.get_sprite()

        return sprites


class SystemWindow(Map2DWindow):
    '''Extends Map2DWindow to display a system'''
    system = None

    def __init__(self, *args, **kwargs):
        system = kwargs.get('system')

        kwargs['map2d'] = system.map
        super(SystemWindow, self).__init__(*args, **kwargs)
        self.system = system

    def get_sprite_map(self, interpolation):
        return self.system.get_sprites()
