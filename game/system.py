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

    objects = []

    def __init__(self):
        pass
