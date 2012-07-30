from engine.render import Sprite
from pygame.surface import Surface
from pygame import draw, transform
from engine.structures import Vec2d, Heading
import math


class RigidBody(object):
    mass = 10  # in kilograms
    vector = None
    acceleration = None

    def __init__(self):
        self.vector = Vec2d((0, 0))
        self.acceleration = Vec2d((0, 0))

    def update(self, dt):
        self.vector += self.acceleration
        cur_pos = self.get_position()
        
        new_pos = (cur_pos[0] + self.vector[0], cur_pos[1] - self.vector[1])

        self.map.move_object(self, new_pos)

    def apply_force(self, amount, heading):
        theta = math.radians(heading)

        x = round(math.sin(theta) * amount, 2)
        y = round(math.cos(theta) * amount, 2)

        vector = Vec2d((x, y))
        self.acceleration += vector

    def apply_vector(self, vector):
        self.acceleration += vector


class OrientedBody(RigidBody):
    def __init__(self):
        RigidBody.__init__(self)
        self.heading = Heading(0)

    def apply_relative_impulse(self, relative_heading, amount):
        actual_heading = self.heading + relative_heading
        self.apply_force(amount, actual_heading)

    def apply_turn(self, amount):
        self.heading += amount
        return self.heading


class Thruster(object):
    def __init__(self, power=None):
        self.power = power

    on = False
    

class Ship(OrientedBody):
    size = 100
    max_turn_rate = 10
    turning_left = False
    turning_right = False
    _ordered_heading = None
    
    def __init__(self):
        OrientedBody.__init__(self)
        self.heading = Heading(0)

        #orientation is the direction the nozzle is facing
        self.thrusters = {
            'main': {
                'engine': Thruster(power=2),
                'orientation': 180
            },
            'retro': {
                'engine': Thruster(power=1),
                'orientation': 0
            },
            'left': {
                'engine': Thruster(power=1),
                'orientation': 270
            },
            'right': {
                'engine': Thruster(power=1),
                'orientation': 90
            }
        }

    def order_heading(self, heading):
        self._ordered_heading = Heading(heading)

    def update(self, dt):
        #TODO: tidy up ordered_heading stuff
        if self._ordered_heading is not None:
            self.turning_left = False
            self.turning_right = False

            ordered = self._ordered_heading.value
            current = self.heading.value

            if ordered != current:
                #convert to relative heading
                relative = Heading(ordered - current)
                if relative.value < 180:
                    self.turning_right = True
                    distance = relative.value
                else:
                    self.turning_left = True
                    distance = 360 - relative.value

                if distance > self.max_turn_rate:
                    turn_rate = self.max_turn_rate
                else:
                    turn_rate = distance
        else:
            turn_rate = self.max_turn_rate

        if self.turning_left and not self.turning_right:
            self.apply_turn(-turn_rate)
        elif self.turning_right and not self.turning_left:
            self.apply_turn(+turn_rate)

        self.acceleration = Vec2d(0, 0)
        for thruster in self.thrusters:
            engine = self.thrusters[thruster]['engine']
            orientation = self.thrusters[thruster]['orientation'] + 180

            if engine.on:
                self.apply_relative_impulse(orientation, engine.power)

        RigidBody.update(self, dt)

    def set_thruster(self, name, on):
        self.thrusters[name]['engine'].on = on

    def start_turn_left(self):
        self.turning_left = True

    def stop_turn_left(self):
        self.turning_left = False

    def start_turn_right(self):
        self.turning_right = True

    def stop_turn_right(self):
        self.turning_right = False

    def get_sprite(self, scale):
        return build_ship_sprite(
            scale=scale,
            orientation=self.heading,
            size=self.size,
            main_engine=self.thrusters['main']['engine'].on,
            retro_engine=self.thrusters['retro']['engine'].on
        )


def build_ship_sprite(size=None, scale=None, orientation=None, heading=None, main_engine=False, retro_engine=False):
    ship_height = int(round(size * scale))
    if ship_height <= 0:
        ship_height = 9

    width = ship_height / 3

    flame_height = ship_height / 5
    image_width = width
    image_height = ship_height + (flame_height * 2)

    sprite = Sprite()
    sprite.layer = 10
    surface = Surface((image_width, image_height))
    surface.set_colorkey((0, 0, 0))

    ship_top = flame_height
    ship_bottom = image_height - flame_height
    ship_left = 0
    ship_right = image_width
    ship_middle = image_width / 2

    ship_triangle = [(ship_middle, ship_top), (ship_left, ship_bottom), (ship_right, ship_bottom)]
    draw.polygon(surface, (255, 255, 255), ship_triangle)

    if main_engine:
        bottom_flame = [(ship_middle, ship_bottom), (0, image_height), (image_width, image_height)]
        draw.polygon(surface, (255, 255, 0), bottom_flame)

    if retro_engine:
        top_flame = [(ship_middle, ship_top), (0, 0), (image_width, 0)]
        draw.polygon(surface, (255, 255, 0), top_flame)

    rotated_surface = transform.rotate(surface, -orientation)

    sprite.image = rotated_surface

    return sprite
