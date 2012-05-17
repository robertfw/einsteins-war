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

    # most characteristics of stars can be derived from their initial mass and their current age
    # age is in millions of years, initial_mass is in solar masses
    age = None
    initial_mass = None

    # if the star is orbiting a barycenter (for example in a binary system etc), it has an orbit
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
        self.map.add_object(star, (200, 200))
