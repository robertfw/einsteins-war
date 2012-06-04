from __future__ import division
from engine.core import GameCore
from engine.widgets import TextWidget
from pygame.locals import K_ESCAPE, K_w, K_a, K_s, K_d, K_q, K_e
import pygame
from game.galaxy import GalaxyWindow, Galaxy
from game import commands
from game.units import AU, LY
from game import systems


class Game(GameCore):

    def __init__(self, *args, **kwargs):
        super(Game, self).__init__(*args, **kwargs)

        def convert_scale():
            amount = 1 / self.galaxy_window.scale * self.display.resolution[0]

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

        fps_display = TextWidget(binding=lambda: '{fps} fps'.format(fps=self.clock.fps), font_size=20, color=(100, 255, 100))
        ups_display = TextWidget(binding=lambda: '{ups} ups'.format(ups=self.clock.ups), font_size=20, color=(100, 100, 255))
        scale_display = TextWidget(binding=convert_scale, font_size=20, color=(255, 100, 100))

        center_display = TextWidget(binding=lambda: 'c: {center}'.format(center=self.galaxy_window.center), font_size=20, color=(255, 100, 100))
        slice_display = TextWidget(binding=lambda: 'slice: {slice}'.format(slice=self.galaxy_window._slice_rect), font_size=20, color=(255, 100, 100))

        widget_x = self.display.resolution[0]
        widget_y = self.display.resolution[1]
        widget_spacing = 15

        widgets = [fps_display, ups_display, scale_display, center_display, slice_display]
        for i in range(len(widgets)):
            self.widgets.add_widget(widgets[i], (widget_x, widget_y - (widget_spacing * i)))

        #any global keybinds go here (for now)
        self.keyboard.bindings = {
            K_ESCAPE: commands.quit
        }

        #create a new window, make it the full size of our current display
        self.galaxy = Galaxy()
        self.galaxy_window = GalaxyWindow(system=self.galaxy, rect=((0, 0), self.display.resolution), game=self)
        self.windows.add_window(self.galaxy_window)
        self.galaxy_window.scale = 0.000000001
        
        #add some objects
        systems.sol(self.galaxy)
        systems.alpha_centauri(self.galaxy)

        self.register_update_callback(self.galaxy.update)

        #add some keybinds for moving/zooming
        pan_speed = 500
        zoom_speed = 1.1

        self.keyboard.bindings = {
            K_w: {
                'up': lambda: self.galaxy_window.adjust_pan_vector((0, pan_speed)),
                'down': lambda: self.galaxy_window.adjust_pan_vector((0, -pan_speed)),
            },
            K_a: {
                'up': lambda: self.galaxy_window.adjust_pan_vector((pan_speed, 0)),
                'down': lambda: self.galaxy_window.adjust_pan_vector((-pan_speed, 0)),
            },
            K_s: {
                'up': lambda: self.galaxy_window.adjust_pan_vector((0, -pan_speed)),
                'down': lambda: self.galaxy_window.adjust_pan_vector((0, pan_speed)),
            },
            K_d: {
                'up': lambda: self.galaxy_window.adjust_pan_vector((-pan_speed, 0)),
                'down': lambda: self.galaxy_window.adjust_pan_vector((pan_speed, 0)),
            },
            K_e: {
                'up': lambda: self.galaxy_window.adjust_zoom_vector(zoom_speed),
                'down': lambda: self.galaxy_window.adjust_zoom_vector(-zoom_speed)
            },
            K_q: {
                'up': lambda: self.galaxy_window.adjust_zoom_vector(-zoom_speed),
                'down': lambda: self.galaxy_window.adjust_zoom_vector(zoom_speed)
            },
            K_ESCAPE: {
                'down': commands.quit
            }
        }

Game((0, 0), pygame.FULLSCREEN).run()
#Game((800, 800)).run()
