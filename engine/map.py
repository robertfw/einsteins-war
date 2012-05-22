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
            x_bound_low = pos[0] > rect.left
            x_bound_high = pos[0] < rect.right
            y_bound_low = pos[1] > rect.top
            y_bound_high = pos[1] < rect.bottom
            
            if x_bound_low and x_bound_high and y_bound_low and y_bound_high:
                objects[pos] = self.objects[pos]

        return objects


class Map2DWindow(Window):
    '''A map window displays a map, with ability to pan/zoom'''
    _map2d = None  # link to a Map object
    _zoom = 0  # zoom, 0% = full map 100% = ?
    _slice_rect = None  # calculated from zoom & map extent, area of map to show
    
    def __init__(self, *args, **kwargs):
        #TODO: add some validation checking here
        self._map2d = kwargs.get('map2d')
        self._slice_rect = Rect(kwargs.get('rect'))
        self._slice_rect.center = (0, 0)

        super(Map2DWindow, self).__init__(*args, **kwargs)

    @property
    def zoom(self):
        return self._zoom

    @zoom.setter
    def zoom(self, value):
        if value > 100 or value < 0:
            raise ValueError('Zoom out of range 0 <= value <= 100')

        if self._zoom != value:
            self._zoom = value
            self._update_rect()

    def _update_rect(self):
        '''Update our rect based on zoom and maximum extent'''
        pass
