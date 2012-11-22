from __future__ import division
from engine.render import Window
from engine.rect import Rect
from pygame import gfxdraw
from game.units import AU, LY


class Map2D(object):
    '''A representation of objects in a 2d physical space'''
    _map = {}
    _pos_index = {}
    _obj_cache = {}

    def add_object(self, obj, pos):
        key = id(obj)

        #TODO: is adding object attributes like this this bad form?
        #(it sure is nice to be able to just do it!)
        obj.map = self
        obj.get_position = lambda: self.get_position(obj)

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

        #TODO: this could do with some optimizing
        for pos in self._map:
            within_left = pos[0] >= rect.left
            within_right = pos[0] <= rect.right
            within_top = pos[1] >= rect.top
            within_bottom = pos[1] <= rect.bottom

            if within_left and within_right and within_top and within_bottom:
                objects[pos] = self._obj_cache[self._map[pos]]

        return objects


class Map2DWindow(Window):
    '''A map window displays a map, with ability to pan/zoom'''
    map2d = None  # link to a Map object
    game = None  # link to the main game object. TODO: is this ok structurally?
    _scale = 1  # pixels per map unit
    _center = None  # where is the view centered
    _slice_rect = None  # calculated from scale & center, area of map to show
    _dirty_slice = True  # whether we need to update our slice rect
    _pan_vector = (0, 0)  # describes movement of the center
    delta_zoom = 0  # describes movement in zoom
    _viewable_objects = {}  # stores objects/interpolated positions in between updates

    def __init__(self, *args, **kwargs):
        super(Map2DWindow, self).__init__(*args, **kwargs)

        self.map2d = kwargs.get('map2d')
        self.game = kwargs.get('game')

        self.center = (0, 0)

        self._dirty_slice = True

        self._update_slice_rect()

    #TODO: revisit this and the convert_scale function to see if they make sense to be here
    def get_viewport_range(self):
            return '{width} x {height}'.format(width=self.convert_scale(self.rect.right), height=self.convert_scale(self.rect.height))

    def convert_scale(self, width):
        amount = 1 / self.scale * width

        if amount > LY:
            amount = amount / LY
            units = 'ly'
        elif amount > AU:
            amount = amount / AU
            units = 'au'
        elif amount > 1000:
            amount = amount / 1000
            units = 'km'
        else:
            units = 'm'

        amount = round(amount, 2)

        return '{amount:,.2f}{units}'.format(amount=amount, units=units)

    def draw_grid(self, display):
        spacing = 100

        if self._slice_rect is None:
            return

        left = self._slice_rect.left
        top = self._slice_rect.top

        start_left = int(left + left % spacing)
        start_top = int(top + top % spacing)

        screen_start = self.convert_world_to_screen((start_left, start_top))
        screen_left = screen_start[0]
        screen_top = screen_start[1]
        screen_spacing = int(spacing * self.scale)

        for x in range(screen_left, self.rect.right, screen_spacing):
            for y in range(screen_top, self.rect.bottom, screen_spacing):
                gfxdraw.pixel(display.window, x, y, (255, 255, 255))

    def convert_world_to_screen(self, pos):
        #find the relative position in the slice rectangle
        x_relative = (pos[0] - self._slice_rect.left) / self._slice_rect.width
        y_relative = (pos[1] - self._slice_rect.top) / self._slice_rect.height

        #find the matching relative position in the screen
        x = int(self.rect.width * x_relative)
        y = int(self.rect.height * y_relative)

        return (x, y)

    def convert_screen_to_world(self, pos):
        #find the relative position in the window
        x_relative = (pos[0] - self.rect.left) / self.rect.width
        y_relative = (pos[1] - self.rect.top) / self.rect.height

        #find the matching relative position in the slice
        x = self._slice_rect.left + int(self._slice_rect.width * x_relative)
        y = self._slice_rect.top + int(self._slice_rect.height * y_relative)

        return (x, y)

    def _update_slice_rect(self):
        #take our screen dimensions and blow them up according to our scale
        width = self.rect.width / self.scale
        height = self.rect.height / self.scale

        #calculate our left and top values
        top = self.center[1] - (height / 2)
        left = self.center[0] - (width / 2)

        self._slice_rect = Rect(((top, left), (width, height)))
        self._dirty_slice = False

    def get_sprite_map(self, interpolation):
        if interpolation == 0:
            #we're not interpolating - get fresh objects
            self._viewable_objects = self.get_objects()
        else:
            #TODO: implement interpolation
            pass

        display_scale = self.scale

        layers = []

        for pos in self._viewable_objects:
            obj = self._viewable_objects[pos]

            #ask for forgiveness, not for permission
            try:
                sprite = obj.get_sprite(display_scale)

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

    def get_objects(self):
        if self._dirty_slice:
            self._update_slice_rect()

        raw = self.map2d.get_objects_in_rect(self._slice_rect)

        # we need to convert the map co-ordinates to window co-ordinates
        objects = {}
        for pos in raw:
            objects[self.convert_world_to_screen(pos)] = raw[pos]

        return objects

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, value):
        if value <= 0:
            raise ValueError('Scale must be > 0')

        self._scale = value
        self._dirty_slice = True

    @property
    def center(self):
        return self._center

    @center.setter
    def center(self, value):
        self._center = value
        self._dirty_slice = True

    def pan(self, amount):
        self.center = (self.center[0] + amount[0], self.center[1] + amount[1])

    def zoom_in(self, amount):
        self.scale = self.scale * amount

    def zoom_out(self, amount):
        self.scale = self.scale / amount

    def adjust_zoom_vector(self, amount):
        original = self.delta_zoom
        new = original + amount

        if original == 0 and new != 0:
            self.game.register_update_callback(self.update_scale)
        elif original != 0 and new == 0:
            self.game.unregister_update_callback(self.update_scale)

        self.delta_zoom = new

    def update_scale(self, dt):
        #TODO: right now this doesn't adjust for varying delta times
        #its not as simple as pan!
        if self.delta_zoom < 0:
            self.zoom_out(self.delta_zoom * -1)
        elif self.delta_zoom > 0:
            self.zoom_in(self.delta_zoom)

    @property
    def pan_vector(self):
        return self._pan_vector

    @pan_vector.setter
    def pan_vector(self, new):
        original = self._pan_vector

        if original == (0, 0) and new != (0, 0):
            self.game.register_update_callback(self.update_center)
        elif original != (0, 0) and new == (0, 0):
            self.game.unregister_update_callback(self.update_center)

        self._pan_vector = new

    def lock_center(self, obj):
        self._locked_object = obj
        self.game.register_update_callback(self.update_center)

    def unlock_center(self):
        self._locked_object = None
        self.game.unregister_update_callback(self.update_center)

    def update_center(self, dt):
        if self._locked_object is not None:
            self.center = self._locked_object.get_position()
        else:
            self.center = (self.center[0] + self.pan_vector[0] * dt, self.center[1] + self.pan_vector[1] * dt)

    def start_panning_left(self, base_speed):
        self.pan_vector = (-base_speed / self.scale, self.pan_vector[1])

    def stop_panning_left(self):
        self.pan_vector = (0, self.pan_vector[1])

    def start_panning_right(self, base_speed):
        self.pan_vector = (+base_speed / self.scale, self.pan_vector[1])

    def stop_panning_right(self):
        self.pan_vector = (0, self.pan_vector[1])

    def start_panning_up(self, base_speed):
        self.pan_vector = (self.pan_vector[0], -base_speed / self.scale)

    def stop_panning_up(self):
        self.pan_vector = (self.pan_vector[0], 0)

    def start_panning_down(self, base_speed):
        self.pan_vector = (self.pan_vector[0], +base_speed / self.scale)

    def stop_panning_down(self):
        self.pan_vector = (self.pan_vector[0], 0)
