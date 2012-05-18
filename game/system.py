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
        sprite.set_base_image(surface)

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
        star = Star()
        self.map.add_object(star, (200, 200))

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

    def __init__(self, system):
        super(SystemWindow, self).__init__(system.map)
        self.system = system

    def render(self, renderer):
        sprites = self.system.get_sprites()
        renderer.draw_sprite_map(sprites)
