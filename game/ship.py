from engine.render import Sprite
from pygame.surface import Surface
from engine.utils import memoize
from pygame import draw, transform
from engine.vectors import Vec2d
import math


class Heading(object):
    angle = 0

    def __init__(self, angle=0):
        self.set_angle(angle)

    def __repr__(self):
        return str(self.angle)
    
    def set_angle(self, angle):
        #TODO: currently deals with large angles by recursion, better method?
        if angle > 360:
            angle -= 360
            self.set_angle(angle)
        elif angle < 0:
            angle += 360
            self.set_angle(angle)
        else:
            self.angle = angle
  
    #TODO: implement __add__, __subtract__, etc
    def add(self, degrees):
        self.set_angle(self.angle + degrees)
   
        return self.angle


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
        new_pos = (cur_pos[0] + self.vector[0], cur_pos[1] + self.vector[1])
        #print 'moving to {pos}'.format(pos=new_pos)

        self.map.move_object(self, new_pos)

    def apply_force(self, heading, amount):
        theta = math.radians(heading)

        x = round(math.sin(theta) * amount, 2)
        y = round(math.cos(theta) * amount, 2)

        vector = Vec2d((x, y))
        self.acceleration += vector

    def apply_vector(self, vector):
        self.acceleration += vector


class OrientedBody(RigidBody):
    def __init__(self):
        #TODO: investigate use of super, whether it should be used, etc
        RigidBody.__init__(self)
        self.heading = Heading()

    def apply_relative_impulse(self, heading, amount):
        self.apply_force(amount, self.heading.add(heading))

    def apply_turn(self, amount):
        self.heading.add(amount)
        return self.heading.angle


class Thruster(object):
    on = False
    power = 10


class Ship(OrientedBody):
    size = 10
    turn_rate = .5
    turning_left = False
    turning_right = False
    
    def __init__(self):
        #TODO: investigate use of super, whether it should be used, etc
        OrientedBody.__init__(self)

        self.thrusters = {
            'main': {
                'engine': Thruster(),
                'orientation': 180
            },
            'retro': {
                'engine': Thruster(),
                'orientation': 0
            }
        }

    def update(self, dt):
        if self.turning_left and not self.turning_right:
            self.apply_turn(self.turn_rate)
        elif self.turning_right and not self.turning_left:
            self.apply_turn(-self.turn_rate)

        for thruster in self.thrusters:
            engine = self.thrusters[thruster]['engine']
            orientation = self.thrusters[thruster]['orientation']

            if engine.on:
                self.apply_relative_impulse(engine.power, orientation)

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

    @memoize
    def get_sprite(self, scale):
        height = int(round(self.size * scale))
        width = height / 3
        if height <= 0:
            height = 3
            width = 1

        sprite = Sprite()
        sprite.layer = 10
        surface = Surface((width, height))
        surface.set_colorkey((0, 0, 0))

        points = [(width / 2, 0), (0, height), (width, height)]
        draw.polygon(surface, (255, 255, 255), points)

        transform.rotate(surface, -self.heading.angle)

        sprite.image = surface

        return sprite
