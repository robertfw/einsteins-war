from __future__ import division
from engine.core import GameCore
from engine.widgets import TextWidget
from pygame.locals import K_ESCAPE, K_w, K_a, K_s, K_d, MOUSEMOTION, MOUSEBUTTONDOWN, K_SPACE, KEYDOWN, KEYUP
from engine.map import Map2DWindow
from game import commands
from game.units import AU
from game.systems import milkyway
from game.ship import Ship
import pygame


class Game(GameCore):

    def __init__(self, *args, **kwargs):
        super(Game, self).__init__(*args, **kwargs)

        #create a new window, make it the full size of our current display
        galaxy = milkyway.create()
        galaxy_window = Map2DWindow(map2d=galaxy.map, rect=((0, 0), self.display.resolution), game=self)
        self.windows.add_window(galaxy_window)
        self.register_update_callback(galaxy.update)
        #self.register_pre_render_callback(galaxy_window.draw_grid)

        #add a ship and center the map on it
        player = Ship()
        galaxy.map.add_object(player, (1 * AU, 1 * AU))
        self.register_update_callback(player.update)
        galaxy_window.lock_center(player)
        galaxy_window.scale = 2

        self.keyboard.bindings = {
            K_w: {
                KEYDOWN: lambda: commands.player_main_engine_on(player),
                KEYUP: lambda: commands.player_main_engine_off(player)
            },
            K_s: {
                KEYDOWN: lambda: commands.player_retro_engine_on(player),
                KEYUP: lambda: commands.player_retro_engine_off(player)
            },
            K_a: {
                KEYDOWN: lambda: commands.player_left_engine_on(player),
                KEYUP: lambda: commands.player_left_engine_off(player)
            },
            K_d: {
                KEYDOWN: lambda: commands.player_right_engine_on(player),
                KEYUP: lambda: commands.player_right_engine_off(player)
            },
            K_SPACE: {
                KEYDOWN: lambda: galaxy_window.lock_center(player)
            },
            K_ESCAPE: {
                KEYDOWN: commands.quit
            }
        }

        self.mouse.bindings = {
            MOUSEMOTION: lambda event: commands.set_player_heading_from_mouse(event, galaxy_window, player),
            MOUSEBUTTONDOWN: {
                1: lambda event: commands.set_map_center_from_mouse_click(event, galaxy_window),
                4: lambda event: commands.zoom_map_in(event, galaxy_window, 2),
                5: lambda event: commands.zoom_map_out(event, galaxy_window, 2)
            }
        }

        widgets = []
        widgets.append(TextWidget(binding=lambda: 'view: {view}'.format(view=galaxy_window.get_viewport_range()), font_size=20, color=(255, 100, 100)))
        widgets.append(TextWidget(binding=lambda: 'pos: {x}, {y}'.format(x=int(player.get_position()[0]), y=int(player.get_position()[1])), font_size=20, color=(255, 50, 150)))
        widgets.append(TextWidget(binding=lambda: 'accell: {accell}'.format(accell=player.acceleration), font_size=20, color=(255, 50, 150)))
        widgets.append(TextWidget(binding=lambda: 'vector: {vector}'.format(vector=player.vector), font_size=20, color=(255, 50, 150)))
        widgets.append(TextWidget(binding=lambda: 'heading: {heading}'.format(heading=player.heading), font_size=20, color=(255, 150, 255)))
        #widgets.append(TextWidget(binding=lambda: 'slice: {slice}'.format(slice=galaxy_window._slice_rect), font_size=20, color=(255, 100, 255)))
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
