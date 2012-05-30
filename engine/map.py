from engine.render import Window


class Map2D(object):
    '''A map is a representation of objects in a physical space'''
    _map = {}
    _pos_index = {}
    _obj_cache = {}

    def add_object(self, obj, pos):
        key = id(obj)
        self._obj_cache[key] = obj
        self._map[pos] = key
        self._pos_index[key] = pos
        return key

    def move_object(self, obj, new_pos):
        key = id(obj)
        del(self._map[self._pos_index[key]])
        self._map[new_pos] = key
        self._pos_index[key] = new_pos

    def get_position(self, obj):
        key = id(obj)
        return self._pos_index[key]

    def get_objects_in_rect(self, rect):
        '''return objects within a given rectangle'''
        objects = {}

        top = rect[0][0]
        left = rect[0][1]
        width = rect[1][0]
        height = rect[1][1]

        right = left + width
        bottom = top + height

        for pos in self._map:
            within_left = pos[0] >= left
            within_right = pos[0] <= right
            within_top = pos[1] >= top
            within_bottom = pos[1] <= bottom

            if within_left and within_right and within_top and within_bottom:
                objects[pos] = self._obj_cache[self._map[pos]]

        return objects


class Map2DWindow(Window):
    '''A map window displays a map, with ability to pan/zoom'''
    _map2d = None  # link to a Map object
    _scale = 1  # pixels per map unit
    _center = None  # where is the view centered
    _slice_rect = None  # calculated from scale & center, area of map to show
    
    def __init__(self, *args, **kwargs):
        super(Map2DWindow, self).__init__(*args, **kwargs)

        self._map2d = kwargs.get('map2d')

        self.center = (0, 0)

        self._update_slice_rect()

    def _update_slice_rect(self):
        width = self.rect.width * (1 / self._scale)
        height = self.rect.height * (1 / self._scale)

        if width < self.rect.width:
            width = self.rect.width

        if height < self.rect.height:
            height = self.rect.height

        top = self._center[1] - (height / 2)
        left = self._center[0] - (width / 2)

        self._slice_rect = ((top, left), (width, height))

    def get_objects(self):
        raw = self._map2d.get_objects_in_rect(self._slice_rect)

        # we need to convert the map co-ordinates to window co-ordinates
        objects = {}
        for pos in raw:
            #account for scale
            new_x = pos[0] * self._scale
            new_y = pos[1] * self._scale
            
            #account for slice center offset
            new_x = new_x + self._center[0]
            new_y = new_y + self._center[1]

            #account for window center offset
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

    @property
    def center(self):
        return self._center

    @center.setter
    def center(self, value):
        self._center = value
        self._update_slice_rect()

    def pan(self, amount):
        self.center = (self.center[0] + amount[0], self.center[1] + amount[1])

    def zoom_in(self, amount):
        self.scale = self.scale * amount

    def zoom_out(self, amount):
        self.scale = self.scale / amount
