from __future__ import division
from engine.map import Map2D, Map2DWindow
from engine.render import Sprite
from pygame import draw
from pygame.surface import Surface
import math
from engine.utils import memoize


@memoize
def generate_sphere_sprite(radius, color, scale):
    sprite = Sprite()
    surface = Surface((radius * 2, radius * 2))
    surface.set_colorkey((0, 0, 0))
    draw.circle(surface, color, (radius, radius), radius, 0)
    sprite.image = surface

    return sprite


class Barycenter(object):
    pass


class MassiveSpheroid(object):

    def get_sprite(self, scale):
        return generate_sphere_sprite(self.radius, self.color, scale)


class Moon(MassiveSpheroid):
    mass = None
    radius = 5
    color = (50, 50, 50)


class Planet(MassiveSpheroid):
    mass = None
    radius = 10
    color = (50, 200, 50)


class Star(MassiveSpheroid):
    mass = None
    radius = 25
    color = (255, 255, 50)


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

        self.child.orbit = self

        # determine our angular velocity, in degrees per second
        #self._angular_velocity = 360 / (self.period * 24 * 60 * 60)
        
        #temp debug override. reality is sooooooo slooooooooow
        self._angular_velocity = 360 / (self.period)

    #TODO: i am not wild about having to pass the map in
    #but we need to find out the parent position to set the center
    #possible to move the offsetting to the system.update_orbits method
    #and treat this method as relative to the parent body
    #which could make sense if we use a relative positioning system
    def update_position(self, dt, map2d):
        self._cur_angle += self._angular_velocity * dt

        if self._cur_angle > 360:
            self._cur_angle -= 360

        #my math teacher always said i'd need this some day
        x = math.sin(self._cur_angle) * self.radius
        y = math.cos(self._cur_angle) * self.radius

        center = map2d.get_position(self.parent)

        position = (x + center[0], y + center[1])

        return position


class Galaxy(object):
    '''
    Represents a galaxy
    '''

    map = None
    orbits = []

    def __init__(self):
        self.map = Map2D()

    def update(self, dt):
        for orbit in self.orbits:
            position = orbit.update_position(dt, self.map)
            self.map.move_object(orbit.child, position)


class GalaxyWindow(Map2DWindow):
    '''Extends Map2DWindow to display a galaxy'''
    system = None

    def __init__(self, *args, **kwargs):
        self.system = kwargs.get('system')
        kwargs['map2d'] = self.system.map
        super(GalaxyWindow, self).__init__(*args, **kwargs)

    def get_sprite_map(self, interpolation):
        if interpolation == 0:
            #we're not interpolating - get fresh objects
            self.viewable_objects = self.get_objects()
        else:
            pass

        layers = []
        for pos in self.viewable_objects:
            obj = self.viewable_objects[pos]
                        
            #ask for forgiveness, not for permission
            try:
                sprite = obj.get_sprite(self.scale)

                #TODO: find a way to not have to repeat this line in the except IndexError block
                layers[sprite.layer][pos] = sprite
            except IndexError:
                #thrown when we don't have that layer yet
                #we need to fill in any layers behind us
                for i in range(len(layers), sprite.layer + 1):
                    layers.append({})
                
                layers[sprite.layer][pos] = sprite
            except AttributeError:
                # thrown when the object doesn't have a sprite. don't draw it
                pass
        
        return layers
