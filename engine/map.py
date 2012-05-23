from engine.render import Window
from pygame.rect import Rect
import sys


class Map2D(object):
    '''A map is a representation of objects in a physical space'''
    objects = {}
    max_axis = None

    def __init__(self):
        self.max_axis = sys.maxint

    def add_object(self, obj, pos):
        self.objects[pos] = obj

    def get_objects_in_rect(self, rect):
        '''return objects within a given rectangle'''
        objects = {}
        for pos in self.objects:
            x_bound_low = pos[0] >= rect.left
            x_bound_high = pos[0] <= rect.right
            y_bound_low = pos[1] >= rect.top
            y_bound_high = pos[1] <= rect.bottom

            if x_bound_low and x_bound_high and y_bound_low and y_bound_high:
                objects[pos] = self.objects[pos]

        return objects


class Map2DWindow(Window):
    '''A map window displays a map, with ability to pan/zoom'''
    _map2d = None  # link to a Map object
    _scale = 1  # pixels per map unit
    center = None  # where is the view centered
    _slice_rect = None  # calculated from scale & center, area of map to show
    
    def __init__(self, *args, **kwargs):
        super(Map2DWindow, self).__init__(*args, **kwargs)

        self._map2d = kwargs.get('map2d')

        self.center = (0, 0)

        self._update_slice_rect()

    def _update_slice_rect(self):
        width = self.rect.width * self._scale
        height = self.rect.height * self._scale

        top = self.center[1] - (height / 2)
        left = self.center[0] - (width / 2)

        self._slice_rect = Rect((top, left), (width, height))

    def get_objects(self):
        raw = self._map2d.get_objects_in_rect(self._slice_rect)

        # we need to convert the map co-ordinates to window co-ordinates
        objects = {}
        for pos in raw:
            #account for scale
            new_x = pos[0] * self._scale
            new_y = pos[1] * self._scale
            
            #account for center offset
            new_x = new_x + self.rect.centerx
            new_y = new_y + self.rect.centery
            
            new_pos = (new_x, new_y)
            objects[new_pos] = raw[pos]

        return objects

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, value):
        if value <= 0:
            raise ValueError('Scale must be > 0')

        self._scale = value
        self._update_slice_rect()