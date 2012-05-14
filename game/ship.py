class TriConfig(object):
    '''
    Represents a linked three axis configuration
    '''

    def __init__(self, labels):
        pass


class Vector2D(object):
    '''
    Represents a 2 dimensional vector
    '''

    pass


class Modifier(object):
    '''
    Represents buffs/debuffs
    '''

    attribute = None
    amount = None


class Ship(object):
    '''
    Represents a ship
    '''

    #TODO: should look into using __slots__, we're going to have alot of these ships...

    dumb_mass = None  # how much dumb mass the ship is carrying, in tonnes
    smart_mass = None  # how much smart mass the ship has, in tonnes

    ship_config = TriConfig(('Firepower', 'Engines', 'Armour'))
    cpu_config = TriConfig(('Research', 'Sensors', 'Mass Conversion'))

    modifiers = []

    velocity = Vector2D()
    acceleration = Vector2D()

    def take_damage(self, amount):
        pass

    @property
    def total_mass(self):
        return self.dumb_mass + self.smart_mass

    @property
    def firepower(self):
        pass

    @property
    def engines(self):
        pass

    @property
    def armour(self):
        pass

    @property
    def research(self):
        pass

    @property
    def sensors(self):
        pass

    @property
    def mass_conversion(self):
        pass
