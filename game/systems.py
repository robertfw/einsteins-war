import random
from game.units import KM, AU, LY, YEAR, SR
from game.galaxy import GalaxyFactory, Star, Planet, Moon, Barycenter, Orbit
import math

milkyway = GalaxyFactory()


@milkyway.register
def alpha_centauri(galaxy):
    d = 4.37 * LY
    ac_a = Star(radius=1.2 * SR, color=(255, 250, 230))
    ac_b = Star(radius=.8 * SR, color=(255, 221, 140))
    barycenter = Barycenter()

    galaxy.map.add_object(barycenter, (d, d))
    add_orbiting_object(galaxy, barycenter, ac_a, 10 * AU, 90 * YEAR, 0)
    add_orbiting_object(galaxy, barycenter, ac_b, 10 * AU, 90 * YEAR, 180)

    #some asteroids
    inner_limit = 2.3 * AU
    outer_limit = 3.2 * AU

    inner_period = 700
    outer_period = 2000

    add_asteroid_belt(galaxy, 750, ac_a, inner_limit, outer_limit * 1.2, inner_period, outer_period)
    add_asteroid_belt(galaxy, 450, ac_b, inner_limit, outer_limit, inner_period, outer_period)


@milkyway.register
def sol(galaxy):
    index = {}

    index['sol'] = sol = Star(radius=1 * SR, color=(255, 250, 230))
    galaxy.map.add_object(sol, (0, 0))

    #Mercury
    index['mercury'] = mercury = Planet(radius=2439 * KM, color=(200, 200, 200))
    add_orbiting_object(galaxy, sol, mercury, .46 * AU, 87)

    #Venus
    index['venus'] = venus = Planet(radius=6051 * KM, color=(250, 187, 85))
    add_orbiting_object(galaxy, sol, venus, .7 * AU, 224)

    #Earth
    index['earth'] = earth = Planet(radius=6371 * KM, color=(30, 30, 255))
    add_orbiting_object(galaxy, sol, earth, 1 * AU, 365)

    add_orbiting_object(galaxy, earth, Moon(radius=1700 * KM), 384405 * KM, 29)

    #Mars
    index['mars'] = mars = Planet(radius=3390 * KM, color=(255, 20, 20))
    add_orbiting_object(galaxy, sol, mars, 1.6 * AU, 686)

    add_orbiting_object(galaxy, mars, Moon(radius=11 * KM), 9377 * KM, .3)
    add_orbiting_object(galaxy, mars, Moon(radius=6 * KM), 23460 * KM, 1.2)

    #Jupiter
    index['jupiter'] = jupiter = Planet(radius=69911 * KM, color=(227, 207, 175))
    jupiter.radius = 69911 * KM
    add_orbiting_object(galaxy, sol, jupiter, 5.2 * AU, 4332)
    add_orbiting_object(galaxy, jupiter, Moon(radius=1800 * KM), 421700 * KM, 1.7)
    add_orbiting_object(galaxy, jupiter, Moon(radius=1550 * KM), 671034 * KM, 3.55)
    add_orbiting_object(galaxy, jupiter, Moon(radius=2600 * KM), 1070412 * KM, 7.15)
    add_orbiting_object(galaxy, jupiter, Moon(radius=2400 * KM), 1882709 * KM, 16.69)

    #Saturn
    index['saturn'] = saturn = Planet(radius=58232 * KM, color=(255, 204, 51))
    add_orbiting_object(galaxy, sol, saturn, 10 * AU, 10759)

    add_orbiting_object(galaxy, saturn, Moon(radius=198 * KM), 185000 * KM, 0.9)
    add_orbiting_object(galaxy, saturn, Moon(radius=252 * KM), 238000 * KM, 1.4)
    add_orbiting_object(galaxy, saturn, Moon(radius=531 * KM), 295000 * KM, 1.9)
    add_orbiting_object(galaxy, saturn, Moon(radius=556 * KM), 377000 * KM, 2.7)
    add_orbiting_object(galaxy, saturn, Moon(radius=750 * KM), 527000 * KM, 4.5)
    add_orbiting_object(galaxy, saturn, Moon(radius=2560 * KM), 1222000 * KM, 16)
    add_orbiting_object(galaxy, saturn, Moon(radius=700 * KM), 3560000 * KM, 79)

    inner_period = 200
    outer_period = 250

    add_asteroid_belt(galaxy, 200, saturn, 66900 * KM, 74510 * KM, inner_period, outer_period, 1, 1, (120, 102, 51))
    add_asteroid_belt(galaxy, 500, saturn, 74658 * KM, 92000 * KM, inner_period, outer_period, 1, 1, (105, 102, 91))
    add_asteroid_belt(galaxy, 700, saturn, 92000 * KM, 117580 * KM, inner_period, outer_period, 1, 1, (105, 102, 51))
    add_asteroid_belt(galaxy, 700, saturn, 122170 * KM, 136775 * KM, inner_period, outer_period, 1, 1, (105, 80, 51))

    #Uranus
    index['uranus'] = uranus = Planet()
    uranus.radius = 25362 * KM
    add_orbiting_object(galaxy, sol, uranus, 19 * AU, 30799)
    add_orbiting_object(galaxy, uranus, Moon(), .25 * AU, 30)
    add_orbiting_object(galaxy, uranus, Moon(), .35 * AU, 65)

    #Neptune
    index['neptune'] = neptune = Planet()
    neptune.radius = 24622 * KM
    add_orbiting_object(galaxy, sol, neptune, 30 * AU, 60190)
    add_orbiting_object(galaxy, neptune, Moon(), .25 * AU, 30)

    #the asteroid belt
    add_asteroid_belt(galaxy, 1000, sol, 2.3 * AU, 3.2 * AU, 700, 2000, min_radius=10, max_radius=1000)

    return index


def add_asteroid_belt(galaxy,
                      number,
                      parent,
                      inner_limit,
                      outer_limit,
                      inner_period,
                      outer_period,
                      min_radius=1,
                      max_radius=3,
                      color=None):
    for i in range(number):
        radius = random.uniform(inner_limit, outer_limit)

        period = (outer_period - inner_period) * radius / outer_limit
        asteroid = Moon()
        if color is not None:
            asteroid.color = color
        asteroid.radius = random.randint(min_radius, max_radius)
        add_orbiting_object(galaxy, parent, asteroid, radius, period)


def add_orbiting_object(galaxy, parent, child, distance, period, start_angle=None):
    '''helper function to add an object to the map with an orbit'''

    if start_angle is None:
        start_angle = random.randint(0, 359)

    start_angle = math.radians(start_angle)

    orbit = Orbit(parent=parent, child=child, period=period, angle=start_angle, radius=distance)

    position = orbit.update_position(0)

    galaxy.orbits.append(orbit)
    return galaxy.map.add_object(child, position)
