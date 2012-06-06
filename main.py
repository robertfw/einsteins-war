from __future__ import division
from engine.core import GameCore
from engine.widgets import TextWidget
from pygame.locals import K_ESCAPE, K_w, K_a, K_s, K_d, K_q, K_e
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
            amount = 1 / self.galaxy_window.scale * width

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

        widgets = []
        widgets.append(TextWidget(binding=lambda: 'slice: {slice}'.format(slice=self.galaxy_window._slice_rect), font_size=20, color=(255, 100, 255)))
        widgets.append(TextWidget(binding=lambda: 'view: {view}'.format(view=get_viewport_range()), font_size=20, color=(255, 100, 100)))
        widgets.append(TextWidget(binding=lambda: 'c: {center}'.format(center=self.galaxy_window.center), font_size=20, color=(255, 100, 100)))
        widgets.append(TextWidget(binding=lambda: 'pv: {vector}'.format(vector=self.galaxy_window.pan_vector), font_size=20, color=(255, 100, 255)))
        widgets.append(TextWidget(binding=lambda: '{fps} fps'.format(fps=self.clock.fps), font_size=20, color=(100, 255, 100)))
        widgets.append(TextWidget(binding=lambda: '{ups} ups'.format(ups=self.clock.ups), font_size=20, color=(100, 100, 255)))

        widget_x = self.display.resolution[0]
        widget_y = self.display.resolution[1]
        widget_spacing = 15

        for i in range(len(widgets)):
            self.widgets.add_widget(widgets[i], (widget_x, widget_y - (widget_spacing * i)))

        #any global keybinds go here (for now)
        self.keyboard.bindings = {
            K_ESCAPE: commands.quit
        }

        #create a new window, make it the full size of our current display
        self.galaxy = milkyway.create()
        self.galaxy_window = Map2DWindow(map2d=self.galaxy.map, rect=((0, 0), self.display.resolution), game=self)
        self.windows.add_window(self.galaxy_window)
        
        self.register_update_callback(self.galaxy.update)

        #add a ship and center the map on it
        player = Ship()
        self.galaxy.map.add_object(player, (1 * AU, 1 * AU))
        self.galaxy_window.lock_center(player)
        self.galaxy_window.scale = 2

        # self.keyboard.bindings.update({
        #     K_up: {
        #         'down': lambda: self.galaxy_window.start_panning_up(pan_speed),
        #         'up': lambda: self.galaxy_window.stop_panning_up(),
        #     },
        # })

        #add some keybinds for moving/zooming
        pan_speed = 500
        zoom_speed = 1.1

        self.keyboard.bindings.update({
            K_w: {
                'down': lambda: self.galaxy_window.start_panning_up(pan_speed),
                'up': lambda: self.galaxy_window.stop_panning_up(),
            },
            K_a: {
                'down': lambda: self.galaxy_window.start_panning_left(pan_speed),
                'up': lambda: self.galaxy_window.stop_panning_left(),
            },
            K_s: {
                'down': lambda: self.galaxy_window.start_panning_down(pan_speed),
                'up': lambda: self.galaxy_window.stop_panning_down(),
            },
            K_d: {
                'down': lambda: self.galaxy_window.start_panning_right(pan_speed),
                'up': lambda: self.galaxy_window.stop_panning_right(),
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
        })

Game((0, 0), pygame.FULLSCREEN).run()
#Game((800, 800)).run()
