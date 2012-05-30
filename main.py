from __future__ import division
from engine.core import GameCore
from engine.widgets import TextWidget
from pygame.locals import K_ESCAPE, K_w, K_a, K_s, K_d, K_q, K_e

from game.system import SystemWindow, System
from game import commands


class Game(GameCore):

    def __init__(self, *args, **kwargs):
        super(Game, self).__init__(*args, **kwargs)

        fps_display = TextWidget(binding=lambda: '{fps} fps'.format(fps=self.clock.fps), font_size=20, color=(100, 255, 100))
        ups_display = TextWidget(binding=lambda: '{ups} ups'.format(ups=self.clock.ups), font_size=20, color=(100, 100, 255))
        
        self.widgets.add_widget(fps_display, (800, 600))
        self.widgets.add_widget(ups_display, (800, 585))

        #setup our keyboard controller
        self.keyboard.set_repeat(100, 100)

        #any global keybinds go here (for now)
        self.keyboard.bindings = {
            K_ESCAPE: commands.quit
        }

        self.scale_demo()

    def scale_demo(self):
        #create a new window, make it the full size of our current display
        self.system_window = SystemWindow(system=System(), rect=((0, 0), self.display.resolution))
        self.windows.add_window(self.system_window)
        self.system_window.scale = 0.000000001

        #add a widget to show our current scale
        def convert_scale():
                amount = 1 / self.system_window.scale

                if amount > 1000:
                        amount = amount / 1000
                        units = 'km'
                else:
                        units = 'm'

                amount = round(amount, 2)

                return '1px : {amount:,.2f}{units}'.format(amount=amount, units=units)

        scale_display = TextWidget(binding=convert_scale, font_size=20, color=(255, 100, 100))
        self.widgets.add_widget(scale_display, (800, 570))

        self.register_update_callback(self.system_window.system.update_orbits)

        #add some keybinds for moving/zooming
        pan_speed = 10
        zoom_speed = 1.2
        
        self.keyboard.bindings[K_e] = lambda: self.system_window.zoom_in(zoom_speed)
        self.keyboard.bindings[K_q] = lambda: self.system_window.zoom_out(zoom_speed)
        self.keyboard.bindings[K_w] = lambda: self.system_window.pan((0, pan_speed))
        self.keyboard.bindings[K_s] = lambda: self.system_window.pan((0, -pan_speed))
        self.keyboard.bindings[K_a] = lambda: self.system_window.pan((pan_speed, 0))
        self.keyboard.bindings[K_d] = lambda: self.system_window.pan((-pan_speed, 0))


Game(resolution=(800, 600)).run()
