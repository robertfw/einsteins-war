import random
from game.units import AU, LY, YEAR
from game.galaxy import Star, Planet, Moon, Barycenter, Orbit
import math


def sol_system():
    pass


def alpha_centauri(galaxy):
    d = 4.37 * LY
    ac_a = Star()
    ac_b = Star()
    barycenter = Barycenter()

    galaxy.map.add_object(barycenter, (d, d))
    add_orbiting_object(galaxy, barycenter, ac_a, 10 * AU, 90 * YEAR, 0)
    add_orbiting_object(galaxy, barycenter, ac_b, 10 * AU, 90 * YEAR, 180)

    #some asteroids
    inner_limit = 2.3 * AU
    outer_limit = 3.2 * AU

    #TODO: these are just educated guesses based on mars/jupiter
    inner_period = 700
    outer_period = 2000

    add_asteroid_belt(galaxy, 500, ac_a, inner_limit, outer_limit, inner_period, outer_period)
    add_asteroid_belt(galaxy, 500, ac_b, inner_limit, outer_limit, inner_period, outer_period)


def sol(galaxy):
    sol = Star()
    galaxy.map.add_object(sol, (0, 0))

    #Mercury
    mercury = Planet()
    add_orbiting_object(galaxy, sol, mercury, .46 * AU, 87)

    #Venus
    venus = Planet()
    add_orbiting_object(galaxy, sol, venus, .7 * AU, 224)

    #Earth
    earth = Planet()
    earth.color = (30, 30, 255)
    add_orbiting_object(galaxy, sol, earth, 1 * AU, 365)

    add_orbiting_object(galaxy, earth, Moon(), .15 * AU, 29)

    #Mars
    mars = Planet()
    mars.color = (255, 20, 20)
    add_orbiting_object(galaxy, sol, mars, 1.6 * AU, 686)

    add_orbiting_object(galaxy, mars, Moon(), .15 * AU, 30)
    add_orbiting_object(galaxy, mars, Moon(), .20 * AU, 65)

    #Jupiter
    jupiter = Planet()
    add_orbiting_object(galaxy, sol, jupiter, 5.2 * AU, 4332)
    add_orbiting_object(galaxy, jupiter, Moon(), .25 * AU, 30)
    add_orbiting_object(galaxy, jupiter, Moon(), .35 * AU, 65)
    add_orbiting_object(galaxy, jupiter, Moon(), .40 * AU, 95)
    add_orbiting_object(galaxy, jupiter, Moon(), .50 * AU, 115)

    #Saturn
    saturn = Planet()
    add_orbiting_object(galaxy, sol, saturn, 10 * AU, 10759)
    add_orbiting_object(galaxy, saturn, Moon(), .25 * AU, 30)
    add_orbiting_object(galaxy, saturn, Moon(), .35 * AU, 65)
    add_orbiting_object(galaxy, saturn, Moon(), .40 * AU, 95)
    add_orbiting_object(galaxy, saturn, Moon(), .50 * AU, 115)

    #Uranus
    uranus = Planet()
    add_orbiting_object(galaxy, sol, uranus, 19 * AU, 30799)
    add_orbiting_object(galaxy, uranus, Moon(), .25 * AU, 30)
    add_orbiting_object(galaxy, uranus, Moon(), .35 * AU, 65)

    #Neptune
    neptune = Planet()
    add_orbiting_object(galaxy, sol, neptune, 30 * AU, 60190)
    add_orbiting_object(galaxy, neptune, Moon(), .25 * AU, 30)

    #some asteroids
    inner_limit = 2.3 * AU
    outer_limit = 3.2 * AU

    #TODO: these are just educated guesses based on mars/jupiter
    inner_period = 700
    outer_period = 2000

    add_asteroid_belt(galaxy, 1000, sol, inner_limit, outer_limit, inner_period, outer_period)


def add_asteroid_belt(galaxy, number, parent, inner_limit, outer_limit, inner_period, outer_period):
    for i in range(number):
        radius = random.uniform(inner_limit, outer_limit)

        period = (outer_period - inner_period) * radius / outer_limit
        asteroid = Moon()
        asteroid.radius = 2
        add_orbiting_object(galaxy, parent, asteroid, radius, period)


def add_orbiting_object(galaxy, parent, child, distance, period, start_angle=None):
    '''helper function to add an object to the map with an orbit'''

    if start_angle is None:
        start_angle = random.randint(0, 359)

    start_angle = math.radians(start_angle)

    orbit = Orbit(parent=parent, child=child, period=period, angle=start_angle, radius=distance)

    position = orbit.update_position(0, galaxy.map)

    galaxy.orbits.append(orbit)
    return galaxy.map.add_object(child, position)
