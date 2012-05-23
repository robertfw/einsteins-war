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
            else:
                pass
                #print rect
                #print "{0}, {1}, {2}, {3}".format(x_bound_high, x_bound_low, y_bound_high, y_bound_low)
                #print '----'

        return objects

    def get_extents(self):
        top, bottom, left, right = None, None, None, None

        for pos in self.objects:
            if pos[0] < left or left is None:
                left = pos[0]

            if pos[0] > right or right is None:
                right = pos[0]

            if pos[1] > top or top is None:
                top = pos[1]

            if pos[1] < bottom or bottom is None:
                bottom = pos[1]

        width = right - left
        height = top - bottom

        extents = Rect((left, top), (width, height))
        print extents

        return extents


class Map2DWindow(Window):
    '''A map window displays a map, with ability to pan/zoom'''
    _map2d = None  # link to a Map object
    _zoom = 0  # zoom, 0% = full map 100% = ?
    _slice_rect = None  # calculated from zoom & map extent, area of map to show
    
    def __init__(self, *args, **kwargs):
        #TODO: add some validation checking here
        self._map2d = kwargs.get('map2d')
        
        self._slice_rect = self._map2d.get_extents()

        super(Map2DWindow, self).__init__(*args, **kwargs)

    def get_objects(self):
        return self._map2d.get_objects_in_rect(self._slice_rect)
