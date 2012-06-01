from __future__ import division
from engine.core import GameCore
from engine.widgets import TextWidget
from pygame.locals import K_ESCAPE, K_w, K_a, K_s, K_d, K_q, K_e
import pygame

from game.system import SystemWindow, System
from game import commands


class Game(GameCore):

    def __init__(self, *args, **kwargs):
        super(Game, self).__init__(*args, **kwargs)

        def convert_scale():
                amount = 1 / self.system_window.scale

                if amount > 1000:
                        amount = amount / 1000
                        units = 'km'
                else:
                        units = 'm'

                amount = round(amount, 2)

                return '1px : {amount:,.2f}{units}'.format(amount=amount, units=units)

        fps_display = TextWidget(binding=lambda: '{fps} fps'.format(fps=self.clock.fps), font_size=20, color=(100, 255, 100))
        ups_display = TextWidget(binding=lambda: '{ups} ups'.format(ups=self.clock.ups), font_size=20, color=(100, 100, 255))
        scale_display = TextWidget(binding=convert_scale, font_size=20, color=(255, 100, 100))

        widget_x = self.display.resolution[0]
        widget_y = self.display.resolution[1]
        widget_spacing = 15
        
        self.widgets.add_widget(scale_display, (widget_x, widget_y))
        self.widgets.add_widget(fps_display, (widget_x, widget_y - widget_spacing))
        self.widgets.add_widget(ups_display, (widget_x, widget_y - widget_spacing * 2))

        #any global keybinds go here (for now)
        self.keyboard.bindings = {
            K_ESCAPE: commands.quit
        }

        self.scale_demo()

    def scale_demo(self):
        #create a new window, make it the full size of our current display
        self.system_window = SystemWindow(system=System(), rect=((0, 0), self.display.resolution), game=self)
        self.windows.add_window(self.system_window)
        self.system_window.scale = 0.00000001

        self.register_update_callback(self.system_window.system.update_orbits)

        #add some keybinds for moving/zooming
        pan_speed = 100
        zoom_speed = 1.1

        self.keyboard.bindings = {
            K_w: {
                'up': lambda: self.system_window.adjust_pan_vector((0, pan_speed)),
                'down': lambda: self.system_window.adjust_pan_vector((0, -pan_speed)),
            },
            K_a: {
                'up': lambda: self.system_window.adjust_pan_vector((pan_speed, 0)),
                'down': lambda: self.system_window.adjust_pan_vector((-pan_speed, 0)),
            },
            K_s: {
                'up': lambda: self.system_window.adjust_pan_vector((0, -pan_speed)),
                'down': lambda: self.system_window.adjust_pan_vector((0, pan_speed)),
            },
            K_d: {
                'up': lambda: self.system_window.adjust_pan_vector((-pan_speed, 0)),
                'down': lambda: self.system_window.adjust_pan_vector((pan_speed, 0)),
            },
            K_e: {
                'up': lambda: self.system_window.adjust_zoom_vector(zoom_speed),
                'down': lambda: self.system_window.adjust_zoom_vector(-zoom_speed)
            },
            K_q: {
                'up': lambda: self.system_window.adjust_zoom_vector(-zoom_speed),
                'down': lambda: self.system_window.adjust_zoom_vector(zoom_speed)
            },
            K_ESCAPE: {
                'down': commands.quit
            }
        }

Game((0, 0), pygame.FULLSCREEN).run()
#Game((800, 800)).run()
