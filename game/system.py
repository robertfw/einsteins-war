from engine.physics import Map


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

    age = None
    mass = None
    orbit = None


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
        self.map = Map()
        self.spawn_objects()

    def get_objects(self):
        return self.map.objects

    def spawn_objects(self):
        star = Star()
        self.map.add_object(star, (0, 0))
