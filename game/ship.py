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
        self.heading = Heading(0)

    def apply_relative_impulse(self, heading, amount):
        self.apply_force(amount, self.heading + amount)

    def apply_turn(self, amount):
        self.heading += amount
        return self.heading


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
            self.apply_turn(-self.turn_rate)
        elif self.turning_right and not self.turning_left:
            self.apply_turn(+self.turn_rate)

        self.acceleration = Vec2d(0, 0)
        for thruster in self.thrusters:
            engine = self.thrusters[thruster]['engine']
            orientation = self.thrusters[thruster]['orientation']

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
        return self.build_sprite(scale, self.heading)

    def build_sprite(self, scale, heading):
        print 'building for {scale} @ {heading}'.format(scale=scale, heading=heading)
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
        
        transform.rotate(surface, -heading)

        sprite.image = surface

        return sprite
