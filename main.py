from __future__ import division
from engine.core import GameCore
from engine.widgets import TextWidget
from pygame.locals import K_ESCAPE, K_w, K_a, K_s, K_d, K_q, K_e, K_UP, K_DOWN, K_LEFT, K_RIGHT, MOUSEMOTION
from engine.map import Map2DWindow
from game import commands
from game.units import AU, LY
from game.systems import milkyway
from game.ship import Ship
import pygame


class Game(GameCore):

    def __init__(self, *args, **kwargs):
        super(Game, self).__init__(*args, **kwargs)

        def get_viewport_range():
            return '{width} x {height}'.format(width=convert_scale(self.display.resolution[0]), height=convert_scale(self.display.resolution[1]))

        def convert_scale(width):
            amount = 1 / galaxy_window.scale * width

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

        #any global keybinds go here (for now)
        self.keyboard.bindings = {
            K_ESCAPE: commands.quit
        }

        #create a new window, make it the full size of our current display
        galaxy = milkyway.create()
        galaxy_window = Map2DWindow(map2d=galaxy.map, rect=((0, 0), self.display.resolution), game=self, draw_grid=True, grid_spacing=5)
        self.windows.add_window(galaxy_window)
        
        self.register_update_callback(galaxy.update)

        #add a ship and center the map on it
        player = Ship()
        galaxy.map.add_object(player, (1 * AU, 1 * AU))
        self.register_update_callback(player.update)

        galaxy_window.lock_center(player)
        galaxy_window.scale = 2

        self.keyboard.bindings.update({
            K_w: {
                'down': lambda: player.set_thruster('main', True),
                'up': lambda: player.set_thruster('main', False)
            },
            K_s: {
                'down': lambda: player.set_thruster('retro', True),
                'up': lambda: player.set_thruster('retro', False)
            },
            K_a: {
                'down': lambda: player.set_thruster('strafe_left', True),
                'up': lambda: player.set_thruster('strafe_left', False)
            },
            K_d: {
                'down': lambda: player.set_thruster('strafe_right', True),
                'up': lambda: player.set_thruster('strafe_right', False)
            }
        })

        def set_player_heading_from_mouse(event):
            #convert to be centered around a 0,0 in the middle
            x = event.pos[0] - galaxy_window.rect.centerx
            y = event.pos[1] - galaxy_window.rect.centery

            import math
            theta_rad = math.atan2(y, x)
            degrees = math.degrees(theta_rad)

            #TODO: tidy this up
            if degrees >= 0:
                heading = degrees + 90
            elif degrees < 0:
                if degrees < -90:
                    heading = 360 - abs(degrees) + 90
                else:
                    heading = 90 - abs(degrees)

            if heading == 360:
                heading = 0
            
            heading = round(heading)

            player.order_heading(heading)

        self.mouse.bindings = {
            MOUSEMOTION: set_player_heading_from_mouse
        }

        #add some keybinds for moving/zooming
        #pan_speed = 500
        zoom_speed = 1.1

        self.keyboard.bindings.update({
            # K_w: {
            #     'down': lambda: galaxy_window.start_panning_up(pan_speed),
            #     'up': lambda: galaxy_window.stop_panning_up(),
            # },
            # K_a: {
            #     'down': lambda: galaxy_window.start_panning_left(pan_speed),
            #     'up': lambda: galaxy_window.stop_panning_left(),
            # },
            # K_s: {
            #     'down': lambda: galaxy_window.start_panning_down(pan_speed),
            #     'up': lambda: galaxy_window.stop_panning_down(),
            # },
            # K_d: {
            #     'down': lambda: galaxy_window.start_panning_right(pan_speed),
            #     'up': lambda: galaxy_window.stop_panning_right(),
            # },
            K_e: {
                'up': lambda: galaxy_window.adjust_zoom_vector(zoom_speed),
                'down': lambda: galaxy_window.adjust_zoom_vector(-zoom_speed)
            },
            K_q: {
                'up': lambda: galaxy_window.adjust_zoom_vector(-zoom_speed),
                'down': lambda: galaxy_window.adjust_zoom_vector(zoom_speed)
            },
            K_ESCAPE: {
                'down': commands.quit
            }
        })

        widgets = []
        widgets.append(TextWidget(binding=lambda: 'pos: {pos}'.format(pos=player.get_position()), font_size=20, color=(255, 50, 150)))
        widgets.append(TextWidget(binding=lambda: 'accell: {accell}'.format(accell=player.acceleration), font_size=20, color=(255, 50, 150)))
        widgets.append(TextWidget(binding=lambda: 'vector: {vector}'.format(vector=player.vector), font_size=20, color=(255, 50, 150)))
        widgets.append(TextWidget(binding=lambda: 'heading: {heading}'.format(heading=player.heading), font_size=20, color=(255, 150, 255)))
        #widgets.append(TextWidget(binding=lambda: 'slice: {slice}'.format(slice=galaxy_window._slice_rect), font_size=20, color=(255, 100, 255)))
        #widgets.append(TextWidget(binding=lambda: 'view: {view}'.format(view=get_viewport_range()), font_size=20, color=(255, 100, 100)))
        #widgets.append(TextWidget(binding=lambda: 'c: {center}'.format(center=galaxy_window.center), font_size=20, color=(255, 100, 100)))
        #widgets.append(TextWidget(binding=lambda: 'pv: {vector}'.format(vector=galaxy_window.pan_vector), font_size=20, color=(255, 100, 255)))
        widgets.append(TextWidget(binding=lambda: '{fps} fps'.format(fps=self.clock.fps), font_size=20, color=(100, 255, 100)))
        widgets.append(TextWidget(binding=lambda: '{ups} ups'.format(ups=self.clock.ups), font_size=20, color=(100, 100, 255)))

        widget_x = self.display.resolution[0]
        widget_y = self.display.resolution[1]
        widget_spacing = 15

        for i in range(len(widgets)):
            self.widgets.add_widget(widgets[i], (widget_x, widget_y - (widget_spacing * i)))

#Game((0, 0), pygame.FULLSCREEN).run()
Game((800, 800)).run()
