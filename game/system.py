class Orbit(object):
    '''
    Represents an orbit
    '''

    eccentricity = None


class Star(object):
    '''
    Represents a star (or black hole)
    '''

    age = None
    mass = None

    pass


class Planet(object):
    '''
    Represents a planet
    '''

    age = None
    mass = None

    pass


class DumbMass(object):
    '''
    Represents a lump of collectable mass (asteroids, ship wrecks, etc)
    '''

    mass = None

    pass


class SystemMap(object):
    '''
    Represents a single system
    '''

    def spawn_system(self):
        pass
