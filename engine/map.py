from engine.render import Window
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
        pass


class Map2DWindow(Window):
    '''A map window displays a map, with ability to pan/zoom'''
    _map2d = None  # link to a Map object
    _zoom = 0  # zoom, 0% = full map 100% = ?
    _rect = None  # calculated from zoom & map extent, area of map to show
    
    def __init__(self, *args, **kwargs):
        self._map2d = kwargs.get('map2d')
        super(Map2DWindow, self).__init__(*args, **kwargs)

    @property
    def zoom(self):
        return self._zoom

    @zoom.setter
    def zoom(self, value):
        if value > 100 or value < 0:
            raise ValueError('Zoom out of range 0 <= value <= 100')

        self._zoom = value
        self._update_dimensions()

    def _update_dimensions(self):
        '''Update our dimensions based on zoom and maximum extent'''
        pass
